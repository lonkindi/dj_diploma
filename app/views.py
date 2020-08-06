from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator

from app.forms import LoginForm, ReviewForm
from app.models import Section, Product, Review


def main_view(request):
    template = 'app/index.html'
    context = {'sections': Section.objects.all(),
               'product_list': Product.objects.all()[:3],

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
            # else:
            #     pass
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
    if request.method == 'POST':
        fb_id = request.GET.get('feedback')
        if fb_id:
            review_form = ReviewForm(request.POST or None)
            if review_form.is_valid():
                name = review_form.cleaned_data.get('name')
                text = review_form.cleaned_data.get('text')
                rating = review_form.cleaned_data.get('rating')
                product = Product.objects.filter(id=int(fb_id))[0]
                print('product=', product)
            new_feedback = Review(name=name, text=text, rating=rating, product=product)
            new_feedback.save()
    id = request.GET.get('id')
    if id:
        good = Product.objects.filter(id=int(id))[0]
        if good:
            reviews = Review.objects.filter(product=int(id))
        else:
            template = 'app/empty_section.html'

    form = ReviewForm()
    context = {'sections': sections,
               'good': good,
               'reviews': reviews,
               'form': form,
               }
    return render(request, template_name=template, context=context)


def cart_view(request):
    sections = Section.objects.all()
    my_cart = request.session.get('my_cart', dict())
    status_cart = 'В корзине нет товаров'
    items_cart = []
    if request.method == 'POST':
        id = request.GET.get('id')
        order = request.GET.get('Order')
        clear = request.GET.get('Clear')
        if id:
            # my_cart = request.session.get('my_cart', dict())
            quantity = my_cart.get(id)
            if not quantity:
                quantity = 0
            request.session['my_cart'] = {id: quantity+1}
            request.session.modified = True
            status_cart = 'Товар добавлен в корзину'
        if order:
            print('Order=', type(order))
            status_cart = 'Заказ оформлен'
        if clear:
            if request.session.get('my_cart'):
                del request.session['my_cart']
                status_cart = 'Корзина очищена'


    my_cart = request.session.get('my_cart', dict())
    if my_cart:
        for item in my_cart:
            good = Product.objects.filter(id=int(item))[0]
            quantity = my_cart[item]
            items_cart.append((good.id, good.name, good.inf, quantity))
        status_cart = 'Ваша корзина'
    # else:
    #     status_cart = 'В корзине нет товаров'

    template = 'app/cart.html'
    total_cart = len(items_cart)
    context = {'sections': sections,
               'total_cart': total_cart,
               'items_cart': items_cart,
               'status_cart': status_cart,
               }
    return render(request, template_name=template, context=context)


# def add_cart_view(request):
#     if request.method == 'POST':
#         id = request.GET.get('id')
#         my_cart = request.session.get('my_cart', dict())
#         quantity = my_cart.get(int(id))
#         if not quantity:
#             quantity = 0
#         request.session['my_cart'][id] = quantity+1
#         request.session.modified = True
#         print("request.session['my_cart']=", request.session.get('my_cart'))
#     return HttpResponse(f'Товар добавлен в корзину - {id}')
#     # template = 'app/cart.html'
#     # context = {}
#     # return render(request, template_name=template, context=context)
