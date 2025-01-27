from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .models import MainPage, CarouselImage


def handle_page_not_found(request, exception):
    return render(request, 'main/404.html', status=404)


def index(request):
    main_page = MainPage.objects.filter(is_active=True).first()

    if main_page is None:
        return redirect('goods:index')

    all_carousel_images = CarouselImage.objects.select_related('carousel').all()

    image_availability = {
        image.id: default_storage.exists(image.image.name) for image in all_carousel_images
    }

    carousel_images_map = {}

    for image in all_carousel_images:
        if image_availability.get(image.id, False):
            carousel_images_map.setdefault(image.carousel_id, []).append(image)

    text_blocks = main_page.text_boxes.all()
    content_blocks = main_page.content_boxes.prefetch_related('carousel').all()
    carousel_blocks = main_page.carousel_boxes.prefetch_related('carousel')

    blocks = []

    for block in text_blocks:
        blocks.append((block, 'text'))

    for block in content_blocks:
        block.filtered_images = carousel_images_map.get(block.carousel_id, [])
        if block.filtered_images:
            blocks.append((block, 'content'))

    for block in carousel_blocks:
        block.filtered_images = carousel_images_map.get(block.carousel_id, [])
        if block.filtered_images:
            blocks.append((block, 'carousel'))

    blocks.sort(key=lambda x: x[0].order)

    if not blocks:
        return redirect('goods:index')

    context = {
        'title': 'Главная страница',
        'blocks': blocks,
    }

    return render(request, 'main/index.html', context)
