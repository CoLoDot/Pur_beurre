from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def customizePagination(request, to_paginate, product_by_page):
    """Function to paginate results"""
    paginator = Paginator(to_paginate, product_by_page)
    page = request.GET.get('page')

    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

    return product
