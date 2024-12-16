from django.shortcuts import render
from django.db.transaction import commit
from django.http import HttpResponse
from .forms import UserRegister
from .models import Buyer, Game
def sign_up_by_html(request):
    users = ['Alex', 'Max', 'Nik']
    info = {}
    context = {
        'info': info,
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')
        if password == repeat_password and int(age) >= 18 and username not in users:
            return HttpResponse(f"Приветствуем, {username}!")
        if password != repeat_password:
            info.update({'ERROR1': 'Пароли не совпадают'})
        if int(age) < 18:
            info.update({'ERROR2': 'Вы должны быть старше 18'})
        if username in users:
            info.update({'ERROR3': 'Пользователь уже существует'})
    return render(request, 'registration_page.html', context)

def sign_up_by_django(request):
    info = {}
    form = UserRegister()
    games = Game.objects.all()

    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            try:
                age = int(age)
            except ValueError:
                info['ERROR'] = 'Возраст должен быть числом'
                context = {'info': info, 'form': form, 'games': games}
                return render(request, 'fourth_task/registration_page.html', context)

            if Buyer.objects.filter(name=username).exists():
                info['ERROR'] = 'Пользователь с таким именем уже существует'
            elif age < 18:
                info['ERROR'] = 'Вы должны быть старше 18'
            elif password != repeat_password:
                info['ERROR'] = 'Пароли не совпадают'
            else:
                Buyer.objects.create(name=username, balance=0.00, age=age)
                return HttpResponse(f"Покупатель {username} успешно зарегистрирован!")

    context = {
        'info': info,
        'form': form,
        'games': games,
    }
    return render(request, 'fourth_task/registration_page.html', context)
def main(request):
    title = 'Онлайн магазин настолок'
    text1 = ('Добро пожаловать в магазин настольных игр по популярным играм с компьютера, мы скопировали их, и даже их возростной рейтинг')
    context = {
        'title': title,
        'text1': text1,
    }
    return render(request, 'fourth_task/main_page.html', context)

def shop(request):
    games = Game.objects.all()

    if request.method == "POST":
        game_name = request.POST.get('game_name')

        if 'cart' not in request.session:
            request.session['cart'] = {}

        if game_name in request.session['cart']:
            request.session['cart'][game_name] += 1
        else:
            request.session['cart'][game_name] = 1

        request.session.modified = True

    context = {
        'games': games,
        'cart_items': request.session.get('cart', {}),
    }
    return render(request, 'fourth_task/shop.html', context)

def cart(request):
    cart_items = request.session.get('cart', {})
    return render(request, 'fourth_task/cart.html', {'cart_items': cart_items})