import datetime
import re
import string
from decimal import Decimal

import requests
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect

from bs4 import BeautifulSoup

from core.forms import SignUpForm
from match.models import Match

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
HARDMOB_URL = 'https://www.hardmob.com.br/forums/407-Promocoes'
GATRY_URL = 'https://gatry.com/'
BOLETANDO_URL = 'https://boletando.com/'


# Deprecated. It's only getting links.
def get_match_from_hardmob_page(request, url, headers, interests_list):
    """Tries to find a match on hardmob's page and populate Match object with the data found."""
    page = requests.get(url, headers=headers)
    soup_object = BeautifulSoup(page.content, 'html.parser')
    h3s = soup_object.findAll('h3', {'class': 'threadtitle'})
    links = []
    allow = string.ascii_letters + string.digits
    for h3 in h3s:
        for word in h3.text.split():
            word = re.sub('[^%s]' % allow, '', word).lower()
            if word in interests_list:
                links.append('https://www.hardmob.com.br/' + h3.a.get('href'))


def check_match_already_exists(name, user):
    if Match.objects.filter(name=name, user=user, date_match_found__gte=datetime.date.today()).exists():
        return True
    return False


def handle_gatry_coupon(parent):
    coupon = parent.find('p', {'class': 'comment text-break'})
    if coupon:
        allow = string.ascii_letters + string.digits
        for word in coupon.text.split():
            word = re.sub('[^%s]' % allow, '', word).lower()
            if word == 'cupom':
                return coupon.text.replace(' ', '')
    else:
        return None


def handle_gatry_price(parent):
    price = parent.find('p', {'class': 'price'}).text
    match = re.search('[\d\s.,]*\d', price)
    if match:
        price = match.group(0)
        # For some reason, Gatry's price is in the format 1.234,56. So we need to remove the dot.
        price = price.replace('.', '')
        price = Decimal(price.replace(',', '.'))
        return price

    else:
        return None


def handle_name_length(name):
    if name.__len__() >= 128:
        return name[:127]
    return name


def get_match_from_gatry_page(request, url, headers, interests_list):
    """Tries to find a match on gatry's page and populate Match object with the data found."""
    page = requests.get(url, headers=headers)
    soup_object = BeautifulSoup(page.content, 'html.parser')
    h3s = soup_object.findAll('h3')
    allow = string.ascii_letters + string.digits
    for h3 in h3s:
        for word in h3.text.split():
            word = re.sub('[^%s]' % allow, '', word).lower()
            if word in interests_list:
                """This is basically where the match happens. If there's a match, we'll 
                try to get the name, link, coupon, price and image of the product."""
                name = handle_name_length(h3.text)
                if check_match_already_exists(name, request.user):
                    continue
                link = h3.contents[0].attrs['href']
                coupon = handle_gatry_coupon(h3.parent)
                price = handle_gatry_price(h3.parent)
                image = h3.parent.parent.find('div', {'class': 'image'}).find('a').find('img').attrs['src']
                Match.objects.create(
                    name=name,
                    price=price,
                    link=link,
                    coupon=coupon,
                    user=request.user,
                    image=image,
                )


def handle_boletando_price(price):
    price = price.split(' ')[1]
    price = price.replace('.', '')  # remove dot for values over 1000
    return Decimal(price.replace(',', '.'))


def get_match_from_boletando_page(request, url, headers, interests_list):
    """Tries to find a match on gatry's page and populate Match object with the data found."""
    page = requests.get(url, headers=headers)
    soup_object = BeautifulSoup(page.content, 'html.parser')
    articles = soup_object.findAll('article')
    allow = string.ascii_letters + string.digits
    for article in articles:
        for word in article.find('h3').find('a').text.split():
            word = re.sub('[^%s]' % allow, '', word).lower()
            if word in interests_list:
                """This is basically where the match happens. If there's a match, we'll 
                try to get the name, link, coupon, price and image of the product."""
                name = handle_name_length(article.find('h3').find('a').text)
                if check_match_already_exists(name, request.user):
                    continue
                coupon = ''
                if article.find('div', {'class': 'rehub_offer_coupon'}):
                    coupon = article.find('div', {'class': 'rehub_offer_coupon'}).find('span').text
                link = article.find('h3').find('a').attrs['href']
                price = handle_boletando_price(article.find('span', {'class': 'rh_regular_price'}).text)
                image = article.find('figure').find('img').attrs['src']
                Match.objects.create(
                    name=name,
                    price=price,
                    link=link,
                    coupon=coupon,
                    user=request.user,
                    image=image,
                )


def index(request):

    success = None
    if request.method == 'POST':
        try:
            request.user.keywords = request.POST['tags-1']
            request.user.save()
            interests_list = request.POST['tags-1'].split(',')
            get_match_from_boletando_page(request, BOLETANDO_URL, HEADERS, interests_list)
            get_match_from_gatry_page(request, GATRY_URL, HEADERS, interests_list)
            success = 'Promotions successfully scraped!'
        except:
            error = 'Error trying to scrape for promotions, try again later.'
            return render(request, 'core/index.html', {'error': error})

    return render(request, 'core/index.html', {'matches': Match.objects.filter(user=request.user),
                                               'user': request.user, 'success': success})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')

        return render(request, 'register.html', {'form': form})

    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
