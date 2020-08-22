
import re
import string

import requests

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from bs4 import BeautifulSoup


HARDMOB_URL = 'https://www.hardmob.com.br/forums/407-Promocoes'


def index(request):
    if request.method == 'POST':
        interests_list = request.POST['tags-1'].split(',')
        interval = request.POST['interval']
        hardmob_page = requests.get(HARDMOB_URL)
        soup = BeautifulSoup(hardmob_page.content, 'html.parser')
        h3s = soup.findAll('h3', {'class': 'threadtitle'})
        links = []
        allow = string.ascii_letters + string.digits
        for h3 in h3s:
            for word in h3.text.split():
                word = re.sub('[^%s]' % allow, '', word).lower()
                if word in interests_list:
                    links.append('https://www.hardmob.com.br/'+h3.a.get('href'))
        print(links)
        return render(request, 'core/index.html')
    return render(request, 'core/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

        return render(request, 'register.html', {'form': form})

    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})
