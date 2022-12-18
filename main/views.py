from django.shortcuts import render
from django.views import View


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'index.html', context={'title': 'Pigs Can Fly Labs'})


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html', context={'title': 'About Us'})


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html', context={'title': 'Contact Us'})


class ProductsView(View):
    def get(self, request):
        return render(request, 'products.html', context={'title': 'Products'})


class SubscribeView(View):
    def get(self, request):
        return render(request, 'subscribe_page.html', context={'title': 'Subscribe for updates'})


class ProductView(View):
    def get(self, request):
        return render(request, 'single-product.html', context={'title': 'Product Title'})


