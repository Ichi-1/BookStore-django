from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from django.views.generic import DetailView, ListView



class HomePageView(ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

    # return only available products
    def get_queryset(self):
        qs = Product.products.all()
        return qs


class ProductByCategoryListView(ListView):
    template_name = 'products/categories.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        product = Product.objects.filter(category__slug=category_slug)
        return product


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        category_name = Category.objects.get(slug=category_slug)
        
        context.update({
            'category_name': category_name
        })
        return context
      

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    
    def get_object(self):
        request = self.request
        slug = self.kwargs.get('slug')
        product = Product.objects.filter(slug=slug, in_stock=True).first()
        if not product:
            raise Http404('Product could not be found')
        return product



        




# def index(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'store/home.html', context)


# def category_list(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     products = Product.objects.filter(category=category)
#     return render(request, 'products/categories.html', {'category': category, 'products': products})