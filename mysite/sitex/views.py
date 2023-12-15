from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.models import AnonymousUser

from sitex.models import UserLastCurrency
from .forms import ConvertForm, RegisterForm, LoginForm
import requests




def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect('/login')
    return render(request, "register.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
    return render(request, "login.html", context)






def home_page(request):
    if request.user == AnonymousUser():
        return render(request, 'main.html')
    form = ConvertForm(request.POST or None) 
    if form.is_valid():
        currency1 = request.POST.get('fcurrency', False) 
        currency2 = request.POST.get('scurrency', False) 
        amount = request.POST.get('amount', False) 
        if int(amount) < 0:
            return render(request, 'main.html', {'name': request.user.nickname,
                                                 'form': form})
        url =f"https://api.apilayer.com/exchangerates_data/convert?to={currency2}&from={currency1}&amount={amount}"
        payload = {}
        headers= {
            "apikey": "VtZQE8PguWjixHYT9ZSZR84wl0mJoYWn"
        }
        response = requests.request("GET", url, headers=headers, data=payload).json()
        updated_values = {'currencyto': currency2,
                          'currencyfrom': currency1,
                          'amount': amount,
                         }
        
        UserLastCurrency.objects.update_or_create(
            user_id=request.user.id,
            defaults=updated_values
        )
        context = {'form': form, 
                   'result': response['result'], 
                   'name' : request.user.nickname, } 
        return render(request, 'main.html', context)
    
    return render(request, 'main.html', {'name': request.user.nickname,
                                         'form': form})


def profile_page(request):
    try:
        info = UserLastCurrency.objects.get(user_id=request.user.id)
        context = {
            'name': request.user.nickname,
            'email': request.user.email,
            'role': request.user.role,
            'fcurrency': info.currencyfrom,
            'tcurrency': info.currencyto,
            'amount': info.amount,
        }
    except:
        context = {
            'name': request.user.nickname,
            'email': request.user.email,
            'role': request.user.role,
        }
    return render(request, 'profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')