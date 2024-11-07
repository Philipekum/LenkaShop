from django.shortcuts import render
from .models import MainPage


def order(request):
    return render(request, 'main/order.html')


def handle_page_not_found(request, exception):
    return render(request, 'main/404.html', status=404)


def index(request):
    main_page = MainPage.objects.first() 

    text_blocks = main_page.text_boxes.all()
    content_blocks = main_page.content_boxes.all()

    blocks = []
    
    for block in text_blocks:
        blocks.append((block, 'text'))

    for block in content_blocks:
        blocks.append((block, 'content'))

    blocks.sort(key=lambda x: x[0].order)

    context = {
        'title': 'Главная страница',
        'blocks': blocks 
    }

    return render(request, 'main/index.html', context)
