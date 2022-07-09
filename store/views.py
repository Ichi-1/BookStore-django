from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import (
    Category, Product, 
    ProductSpecification, 
    ProductSpecificationValue
)


class HomePageView(ListView):
    model = Product
    template_name = "store/index.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.prefetch_related('product_image').filter(is_active=True)
        return qs
    
        
        

class ProductByCategoryListView(ListView):
    template_name = "store/categories.html"
    context_object_name = "products"

    def get_queryset(self):
        """
        Return QuerySet of parent category and child categories too
        """
        category_slug = self.kwargs.get('category_slug')
        category = Category.objects.get(slug=category_slug).get_descendants(include_self=True)
        product = Product.objects.filter(category__in=category)
       
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
        product = Product.objects.filter(slug=slug, is_active=True).first()
        if not product:
            raise Http404("Product could not be found")
        return product


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.object.pk

        # check if product already added to wish list
        # then change the context data to button
        in_wish_list = Product.objects.filter(
                users_wishlist=self.request.user, 
                id=product_id
            )

        author = ProductSpecificationValue.objects\
            .filter(specification_id=3)\
            .get(product_id=product_id)

        pages = ProductSpecificationValue.objects\
            .filter(specification_id=2)\
            .get(product_id=product_id)

        isbn = ProductSpecificationValue.objects\
            .filter(specification_id=1)\
            .get(product_id=product_id)

        context.update({
                'author': author, 
                'pages': pages, 
                'isbn': isbn, 
                'in_wish_list': in_wish_list,
            }
        )
        return context