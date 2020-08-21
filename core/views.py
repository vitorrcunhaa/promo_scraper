from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


# def index(request):
#     return render(request, 'billing/index.html')


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
