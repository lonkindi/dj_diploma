import json

from django.contrib.auth import logout, authenticate, login

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator

from app.forms import LoginForm, ReviewForm
from app.models import Section, Product, Review, Article, Order, OrderRelation


def main_view(request):
    template = 'app/index.html'
    context = {'sections': Section.objects.all(),
               'article_list': Article.objects.all(),
               'product_list': Product.objects.all(),
               }
    return render(request, template_name=template, context=context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('user_login', None)
        password = request.POST.get('user_password', None)
        print('username=', username)
        print('password=', password)
        user = authenticate(username=username, password=password)
        print('user=', user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(main_view)
        else:
            return HttpResponse('Invalid login or passpword!')
    template = 'app/registration/login.html'
    form = LoginForm()
    context = {'form': form}
    return render(request, template_name=template, context=context)


def logout_view(request):
    logout(request)
    template = 'app/registration/logout.html'
    context = {}
    return render(request, template_name=template, context=context)


def section_view(request, id=0):
    prod_page = ''
    current_page = ''
    prev_page, next_page = '', ''
    current_section = 0
    sections_page = ''
    template = 'app/empty_section.html'
    sections = Section.objects.all()
    if id:
        try:
            current_section = sections.filter(id=id)[0]
            sections_page = current_section.get_children()
        except IndexError:
            current_section = 0
        if current_section:
            if len(sections_page) == 0:
                current_id = id
                template = 'app/section.html'
                prod_list = Product.objects.filter(section=current_id)
                paginator = Paginator(prod_list, 2)
                current_page = request.GET.get('page', 1)
                prod_page = paginator.get_page(current_page)
                if prod_page.has_previous():
                    prev_page = prod_page.previous_page_number()
                else:
                    prev_page = 1
                if prod_page.has_next():
                    next_page = prod_page.next_page_number()
                else:
                    next_page = paginator.num_pages
    if not current_section:
        current_section = 'Добро пожаловать в Простомагазин!'
    context = {'sections': sections,
               'current_section': current_section,
               'section_page': sections_page,
               'prod_page': prod_page,
               'current_page': current_page,
               'prev_page_url': f'{reverse(section_view)}{id}?page={prev_page}',
               'next_page_url': f'{reverse(section_view)}{id}?page={next_page}',
               }
    return render(request, template_name=template, context=context)


def good_view(request):
    sections = Section.objects.all()
    template = 'app/good.html'
    good = ''
    reviews = ''

    review_left = request.COOKIES.get('review_left')
    if review_left:
        review_left = review_left.replace(r"'", r'"')
        review_left = json.loads(review_left)
        review_list = review_left["you_reviews"]
    else:
        review_list = []
        review_left = {"you_reviews": review_list}
    if request.method == 'POST':
        fb_id = request.GET.get('feedback')
        response = HttpResponseRedirect(f'/good/?id={fb_id}')
        if fb_id and not fb_id in review_list:
            review_form = ReviewForm(request.POST or None)
            if review_form.is_valid():
                name = review_form.cleaned_data.get('name')
                text = review_form.cleaned_data.get('text')
                rating = review_form.cleaned_data.get('rating')
                product = Product.objects.filter(id=int(fb_id))[0]
            new_feedback = Review(name=name, text=text, rating=rating, product=product)
            new_feedback.save()
            review_list.append(int(fb_id))
            print('review_list=', review_list)
            review_left["you_reviews"] = review_list
            review_left = json.dumps(review_left)
            response.set_cookie('review_left', review_left)
            return response

    id = request.GET.get('id')
    if id:
        good = Product.objects.filter(id=int(id))[0]
        if good:
            reviews = Review.objects.filter(product=int(id))
    if good.id in review_left['you_reviews']:
        review_left = True
    else:
        review_left = False
    print('review_left=', review_left, type(review_left))
    form = ReviewForm()
    context = {'sections': sections,
               'good': good,
               'reviews': reviews,
               'review_left': review_left,
               'form': form,
               }
    return render(request, template_name=template, context=context)


def cart_view(request):
    sections = Section.objects.all()
    my_cart = request.COOKIES.get('my_cart', dict())
    if my_cart:
        my_cart = my_cart.replace(r"'", r'"')
        my_cart = json.loads(my_cart)
    status_cart = 'В корзине нет товаров'
    total_price = 0
    items_cart = []
    if request.method == 'POST':
        id = request.GET.get('id')  # add goods to cart
        order = request.GET.get('order')  # confirm order
        clear = request.GET.get('clear')  # clear cart
        if id:
            quantity = my_cart.get(id)
            if not my_cart or not quantity:
                quantity = 0
            else:
                quantity = my_cart.get(id)
            my_cart[id] = quantity + 1
            my_cart = json.dumps(my_cart)
            status_cart = 'Товар добавлен в корзину'
            response = HttpResponseRedirect('./')
            response.set_cookie('my_cart', my_cart)
            return response
        elif order:
            user = request.user.username
            number = len(Order.objects.all()) + 1
            if request.COOKIES.get('my_cart'):
                response = HttpResponseRedirect('./')
                new_order = Order(user=user, number=number)
                new_order.save()
                for item in my_cart:
                    product = Product.objects.filter(id=int(item))[0]
                    quantity = my_cart[item]
                    order_relation = OrderRelation(product=product, order=new_order, quantity=quantity)
                    order_relation.save()
                response.delete_cookie('my_cart')
                return response
        elif clear:
            if request.COOKIES.get('my_cart'):
                response = HttpResponseRedirect('./')
                response.delete_cookie('my_cart')
                return response
    else:
        pass
    my_cart = request.COOKIES.get('my_cart', None)
    if my_cart:
        my_cart = my_cart.replace(r"'", r'"')
        my_cart = json.loads(my_cart)

    if my_cart:
        for item in my_cart:
            good = Product.objects.filter(id=int(item))[0]
            quantity = my_cart[item]
            items_cart.append((good.id, good.name, good.inf, good.price, quantity))
            total_price += good.price * quantity
        status_cart = 'Ваша корзина'
    template = 'app/cart.html'
    total_cart = len(items_cart)

    context = {'sections': sections,
               'total_cart': total_cart,
               'items_cart': items_cart,
               'status_cart': status_cart,
               'total_price': total_price,
               }
    return render(request, template_name=template, context=context)
