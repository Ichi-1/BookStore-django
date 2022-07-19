from django.http import Http404
from django.views.generic import DetailView, ListView

from .models import Category, Product, ProductSpecificationValue


class HomePageView(ListView):
    model = Product
    template_name = "store/index.html"
    context_object_name = "products"
    paginate_by = 5

    def get_queryset(self):
        qs = Product.objects.prefetch_related("product_image").filter(
            is_active=True
        )
        return qs


class ProductByCategoryListView(ListView):
    template_name = "store/categories.html"
    context_object_name = "products"
    paginate_by = 5

    def get_queryset(self):
        """
        Return QuerySet of parent category and child categories too
        """
        category_slug = self.kwargs.get("category_slug")
        category = Category.objects.get(slug=category_slug).get_descendants(
            include_self=True
        )
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
        user = self.request.user

        # check if product already added to wish list
        # then change the context data to button
        if user.is_authenticated:
            in_wish_list = Product.objects.filter(
                users_wishlist=user, id=product_id
            )
        else:
            in_wish_list = None


        """ 
        Hardcode removig - init context data dict based on particular product spec.
        Using for loop to init - is easy to scale both name and value for any kind of products.
        Name is always spec name of related type of product.
        For book - author, language, pages, etc.
        """
        product_specification = {}
        product_specification['in_wish_list'] = in_wish_list

        # range based on number of specs
        for i in range(1,5):
            name = str(ProductSpecification.objects.get(id=i)).lower()
            value = str(ProductSpecificationValue.objects.filter(specification_id=i)\
                .get(product_id=product_id)
            )
            product_specification[name] = value
        
        print(product_specification)


        context.update(product_specification)
        return context
