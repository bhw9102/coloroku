from django.shortcuts import render


def intro(request):
    return render(request, 'session/intro.html')

