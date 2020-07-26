from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.forms import LoginForm
from app.models import Section, Product


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
            else:
                pass
                # Return a 'disabled account' error message
        else:
            return HttpResponse('Invalid login or passpword!')
    # Return an 'invalid login' error message.
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
    sections = '',
    product_list = '',
    current_section = ''
    template = 'app/empty_section.html'
    sections = Section.objects.all()
    if id:
        try:
            current_section = sections.filter(id=id)[0]
        except IndexError:
            current_section = 0
        if current_section:
            current_id = id
            template = 'app/section.html'

            product_list = Product.objects.filter(section=current_id)


            # print('len current_section=', len(current_section))

    context = {'sections': sections,
               'product_list': product_list,
               'current_section': current_section,
               }
    return render(request, template_name=template, context=context)

def good_view(request):
    template = 'app/good.html'
    context = {}
    return render(request, template_name=template, context=context)

# def main_view(request):
#     template = 'app/empty_section.html'
#     context = {}
#     return render(request, template_name=template, context=context)