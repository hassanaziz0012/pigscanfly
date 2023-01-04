from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.utils import generate_username
from main.models import Cart, Product, CartProduct, Subscriber
from main.payments import Payments


# Create your views here.
class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'index.html', context={'title': 'Pigs Can Fly Labs', 'products': products})


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html', context={'title': 'About Us'})


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html', context={'title': 'Contact Us'})


class ProductsView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'products.html', context={'title': 'Products', 'products': products})


class SubscribeView(View):
    def get(self, request):
        subbed = request.GET.get('sub')
        return render(request, 'subscribe_page.html', context={'title': 'Subscribe for updates', 'subbed': subbed})

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        next_page = request.POST.get('next')

        try:
            subscriber = Subscriber.objects.get(email=email)
        except Subscriber.DoesNotExist:
            subscriber = Subscriber.objects.create(name=name, email=email)
            subscriber.save()

        return redirect(next_page)


class ProductView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'single-product.html', context={'title': product.name, 'product': product})


class SignupView(View):
    def get(self, request):
        in_use = request.GET.get('in_use', 'false')
        print(in_use)
        return render(request, 'signup.html', context={'title': 'Sign Up', 'in_use': in_use})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            return redirect(reverse('signup') + '?in_use=true')

        except User.DoesNotExist:
            username = generate_username(email)
            user = User.objects.create(email=email, username=username)
            user.set_password(password)
            user.save()

            cart = Cart.objects.create(user=user)
            cart.save()

            login(request, user)
            return redirect('home')
        

class LoginView(View):
    def get(self, request):
        valid = request.GET.get('valid')
        return render(request, 'login.html', context={'title': 'Log In', 'valid': valid})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect(reverse('login') + '?valid=false')
        except User.DoesNotExist:
                return redirect(reverse('login') + '?valid=false')


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
        

@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        total_price = sum(list(cart.products.all().values_list('price', flat=True)))
        return render(request, 'cart.html', context={'title': 'Cart', 'products': cart.products.all(), 'total_price': total_price})


@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def get(self, request, product_id, price):
        product = Product.objects.get(pk=product_id)
        cart = Cart.objects.get(user=request.user)
        quantity = int(float(price) / product.price)

        try:
            cart_product = CartProduct.objects.get(cart=cart, product=product)
        except CartProduct.DoesNotExist:
            cart_product = CartProduct.objects.create(cart=cart, product=product, price=price, quantity=quantity)
            cart_product.save()

        cart.products.add(cart_product)
        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    def get(self, request, product_id):
        cart_product = CartProduct.objects.get(pk=product_id)
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(cart_product)
        cart_product.delete()
        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        redirect_url = Payments.checkout(request, cart)
        return redirect(redirect_url)


@method_decorator(login_required, name='dispatch')
class CheckoutSuccessView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        cart.clear()
        return render(request, 'checkout_success.html', context={'title': 'Success! - Checkout'})


@method_decorator(login_required, name='dispatch')
class CheckoutCancelView(View):
    def get(self, request):
        return render(request, 'checkout_cancel.html', context={'title': 'Cancelled! - Checkout'})
