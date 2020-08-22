import re
import string

import requests
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect

from bs4 import BeautifulSoup

from core.forms import SignUpForm

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
                    links.append('https://www.hardmob.com.br/' + h3.a.get('href'))
        print(links)
        return render(request, 'core/index.html')
    return render(request, 'core/index.html')


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
