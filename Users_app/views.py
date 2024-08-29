from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, ProfileForm, LoginForm
from .models import User, Profile
from Food.models import Pizza, Burger, Pasta, Salad, Appetizer, Drink, Food, Cart,CartItem, OrderFood,OrderItem
from django.contrib.auth.models import AnonymousUser


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # کاربر ثبت شده را لاگین می‌کند
            return redirect('make_profile')  # اطمینان حاصل کن که 'make_profile' در urls.py ثبت شده
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # اتصال پروفایل به کاربر لاگین شده
            profile.save()

            pizzas = Pizza.objects.all()
            burgers = Burger.objects.all()
            pastas = Pasta.objects.all()
            salads = Salad.objects.all()
            appetizers = Appetizer.objects.all()
            drinks = Drink.objects.all()

            context = {
                'pizzas': pizzas,
                'burgers': burgers,
                'pastas': pastas,
                'salads': salads,
                'appetizers': appetizers,
                'drinks': drinks,
                'profile': profile
            }
            return render(request, 'home.html', context=context)
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_phone = form.cleaned_data['username_or_phone']
            password = form.cleaned_data['password']
            
            user = None
            try:
                user = User.objects.get(username=username_or_phone)
            except User.DoesNotExist:
                try:
                    user =User.objects.get(phone_number=username_or_phone)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)

                    # فقط در صورتی که کاربر لاگین شده باشد، پروفایل را بگیرید
                    if not isinstance(request.user, AnonymousUser):
                        profile = Profile.objects.get(user=user)
                    
                    # دریافت داده‌های غذا
                    pizzas = Pizza.objects.all()
                    burgers = Burger.objects.all()
                    pastas = Pasta.objects.all()
                    salads = Salad.objects.all()
                    appetizers = Appetizer.objects.all()
                    drinks = Drink.objects.all()

                    context = {
                        'pizzas': pizzas,
                        'burgers': burgers,
                        'pastas': pastas,
                        'salads': salads,
                        'appetizers': appetizers,
                        'drinks': drinks,
                        'profile': profile
                    }

                    # ذخیره اطلاعات کاربر در سشن
                    # request.session['username'] = user.username
                    # request.session['phone_number'] = profile.phone_number

                    return render(request, 'home.html', context=context)
                else:
                    form.add_error('password', 'رمز عبور اشتباه است.')
            else:
                form.add_error('username_or_phone', 'کاربری با این اطلاعات یافت نشد.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('menu') 



from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden


def add_to_cart(request, item_type, item_id):
    if request.user.is_staff:
        return redirect('login')
    
    if not request.user.is_authenticated:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    
    model_mapping = {
        'pizza': Pizza,
        'burger': Burger,
        'pasta': Pasta,
        'salad': Salad,
        'appetizer': Appetizer,
        'drink': Drink
    }
    
    item_model = model_mapping.get(item_type)
    if not item_model:
        return redirect('cart')
    
    item = get_object_or_404(item_model, id=item_id)
    
    # فیلتر کردن آیتم‌های موجود در سبد خرید بر اساس نوع غذا
    if item_type == 'pizza':
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            pizza=item,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    elif item_type == 'burger':
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            burger=item,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    elif item_type == 'pasta':
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            pasta=item,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    elif item_type == 'salad':
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            salad=item,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    elif item_type == 'appetizer':
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            appetizer=item,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    elif item_type == 'drink':
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            drink=item,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        return redirect('cart')

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()  # ذخیره تغییرات در دیتابیس
    else:
        cart_item.delete()  # حذف آیتم اگر مقدارش ۱ یا کمتر باشد
    
    return redirect('cart')



@login_required
def cart_view(request):
    
    
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    profile = Profile.objects.get(user=request.user)
    pizzas = Pizza.objects.all()
    burgers = Burger.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    appetizers = Appetizer.objects.all()
    drinks = Drink.objects.all()

    context = {
        'pizzas': pizzas,
        'burgers': burgers,
        'pastas': pastas,
        'salads': salads,
        'appetizers': appetizers,
        'drinks': drinks,
        'profile': profile,
        'cart': cart,
        'items': items
    }


    
    return render(request, 'cart.html', context)


@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        return redirect('cart')
    
    # ایجاد سفارش جدید
    order = OrderFood.objects.create(user=request.user)
    
    # ذخیره کردن اقلام سفارش
    for item in cart.items.all():
        if item.pizza:
            OrderItem.objects.create(
                order=order,
                pizza=item.pizza,
                quantity=item.quantity
            )
        elif item.burger:
            OrderItem.objects.create(
                order=order,
                burger=item.burger,
                quantity=item.quantity
            )
        elif item.pasta:
            OrderItem.objects.create(
                order=order,
                pasta=item.pasta,
                quantity=item.quantity
            )
        elif item.salad:
            OrderItem.objects.create(
                order=order,
                salad=item.salad,
                quantity=item.quantity
            )
        elif item.appetizer:
            OrderItem.objects.create(
                order=order,
                appetizer=item.appetizer,
                quantity=item.quantity
            )
        elif item.drink:
            OrderItem.objects.create(
                order=order,
                drink=item.drink,
                quantity=item.quantity
            )
        item.delete()  # حذف آیتم‌ها از سبد خرید


    return redirect('success_buying')


@login_required
def success_buying(request):
    
    
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    profile = Profile.objects.get(user=request.user)
    pizzas = Pizza.objects.all()
    burgers = Burger.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    appetizers = Appetizer.objects.all()
    drinks = Drink.objects.all()

    context = {
        'pizzas': pizzas,
        'burgers': burgers,
        'pastas': pastas,
        'salads': salads,
        'appetizers': appetizers,
        'drinks': drinks,
        'profile': profile,
        'cart': cart,
        'items': items
    }


    
    return render(request, 'success_buying.html', context)