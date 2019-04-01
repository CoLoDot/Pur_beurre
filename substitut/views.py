import json
import requests
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from .form import Connexion
from .models import Products, Users, Saving


# Create your views here.
def index(request):
    """Return Index page"""
    return render(request, 'substitut/index.html')


def signup(request):
    """Signup function for user"""
    error = False

    if request.method == "POST":
        form = Connexion(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            if email and password:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password)
                user.save()
                users_db = Users.objects.create(email=email,
                                                password=password)
                users_db.save()
            else:
                error = True
    else:
        form = Connexion()

    return render(request, 'substitut/signup.html', locals())


def userlogin(request):
    """LogIn a registred user"""
    error = False

    if request.method == "POST":
        form = Connexion(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username,
                                email=email,
                                password=password)
            login(request, user)
        else:
            error = True

    else:
        form = Connexion()

    return render(request, 'substitut/login.html', locals())


def userlogout(request):
    """Logout a registred user"""
    logout(request)
    return render(request, 'substitut/logout.html', locals())


def mentionslegales(request):
    """Return Mentions légales page"""
    return render(request, 'substitut/mentionslegales.html')


def useraccount(request):
    """Return User account page"""
    user_data = Users.objects.all()
    context = {"user_data": user_data}
    return render(request, 'substitut/useraccount.html', context)


def products(request):
    """Return all products"""
    product = Products.objects.all()
    context = {"product": product}
    return render(request, 'substitut/products.html', context)


def userproducts(request):
    """Return saved products of a user"""

    try:
        user = request.user.email
        products_to_display = Saving.objects.filter(contact=user)
        keys_list = []

        for item in products_to_display:
            keys_list.append(item.product_key)

        product = Products.objects.filter(pk__in=keys_list)

        paginator = Paginator(product, 3)
        page = request.GET.get('page')

        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)
        except EmptyPage:
            product = paginator.page(paginator.num_pages)

        context = {"product": product}

    except:
        product = None
        context = {"product": product}

    return render(request, 'substitut/userproducts.html', context)


def search(request):
    """User's search return the result from query's form on index"""
    query = request.GET.get('query')

    if not query:
        product_list = Products.objects.all()
        paginator = Paginator(product_list, 3)
        page = request.GET.get('page')

        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)
        except EmptyPage:
            product = paginator.page(paginator.num_pages)

        context = {"product": product}
    else:
        product_list = Products.objects.filter(name__icontains=query)

        if not product_list:
            search_url = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms="
                                      + query + "&sort_by=unique_scans_n&page_size=20&json=1")
            response = json.loads(search_url.text)
            for product_index in range(0, int(response['count'])):
                if response['products'][product_index]['states_tags'][1] == 'en:complete':
                    try:
                        get_name = response['products'][product_index]['product_name']
                    except KeyError:
                        get_name = ''
                    try:
                        get_url = response['products'][product_index]['url']
                    except KeyError:
                        get_url = ''
                    try:
                        get_img = response['products'][product_index]['image_front_url']
                    except KeyError:
                        get_img = ''
                    try:
                        get_nutriscore = response['products'][product_index]['nutrition_grades']
                    except KeyError:
                        get_nutriscore = ''

                    if product_index == 10:
                        break

                    Products.objects.create(name=get_name,
                                            nutriscore=get_nutriscore,
                                            picture=get_img,
                                            url=get_url)

        product_list = Products.objects.filter(name__icontains=query)
        paginator = Paginator(product_list, 3)
        page = request.GET.get('page')

        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)

        except EmptyPage:
            product = paginator.page(paginator.num_pages)

        context = {"product": product,
                   "urlp": query}

    return render(request, 'substitut/search.html', context)


#  DOC API OFF : https://en.wiki.openfoodfacts.org/index.php?title=API&oldid=7026

def detail(request, product_id):
    """Details for a product"""
    try:
        product_detail = get_object_or_404(Products, pk=product_id)
        user = request.user.email
        saving = request.POST.get('saving')
        if saving:
            Saving.objects.create(contact=user,
                                  product_key=product_detail.pk)

        context = {'name': product_detail.name,
                   'nutriscore': product_detail.nutriscore,
                   'picture': product_detail.picture,
                   'url': product_detail.url}
    except:
        product_detail = get_object_or_404(Products, pk=product_id)
        context = {'name': product_detail.name,
                   'nutriscore': product_detail.nutriscore,
                   'picture': product_detail.picture,
                   'url': product_detail.url}

    return render(request, 'substitut/detail.html', context)
