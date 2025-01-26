from django.shortcuts import render, redirect
from .models import MainPage


def handle_page_not_found(request, exception):
    return render(request, 'main/404.html', status=404)


def index(request):
    main_page = MainPage.objects.filter(is_active=True).first()

    if main_page is None:
        return redirect('goods:index')

    text_blocks = main_page.text_boxes.all()
    content_blocks = main_page.content_boxes.prefetch_related('images').all()
    carousel_blocks = main_page.carousel_boxes.all()

    blocks = []
    
    for block in text_blocks:
        blocks.append((block, 'text'))

    for block in content_blocks:
        blocks.append((block, 'content'))

    for block in carousel_blocks:
        blocks.append((block, 'carousel'))

    blocks.sort(key=lambda x: x[0].order)

    if not blocks:
        return redirect('goods:index')

    context = {
        'title': 'Главная страница',
        'blocks': blocks,
    }

    return render(request, 'main/index.html', context)
