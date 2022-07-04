from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Category, Product


class HomePageView(ListView):
    model = Product
    template_name = "store/index.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.all()
        return qs


class ProductByCategoryListView(ListView):
    template_name = "store/categories.html"
    context_object_name = "products"

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        product = Product.objects.filter(category__slug=category_slug)
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get("category_slug")
        category_name = Category.objects.get(slug=category_slug)

        context.update({"category_name": category_name})
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/detail.html"
    context_object_name = "product"

    def get_object(self):
        slug = self.kwargs.get("slug")
        product = Product.objects.filter(slug=slug, in_stock=True).first()
        if not product:
            raise Http404("Product could not be found")
        return product
