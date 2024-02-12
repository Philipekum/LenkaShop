from django.shortcuts import render

def index(request):
    context = {
        'title': 'Главная страница',
        'content': 'Some content'
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'content': 'Страница о нас!!))'
    }

    return render(request, 'main/about.html', context)
