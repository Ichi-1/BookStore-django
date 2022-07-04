from tabnanny import verbose
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class Category(MPTTModel):
    """
    Category Table implimented with MPTT.
    """
    name = models.CharField(
        verbose_name=_('Category Name'),
        max_length=255,
        unique=True,
        help_text=_('Required and Unique'),
    )
    slug = models.SlugField(
        verbose_name=_('Caregory safe URL'),
        max_length=255,
        unique=True,
    )
    parent = TreeForeignKey(
        'self',
        related_name='child',
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        oredr_insertion_by = ['name']
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    
    def get_absolute_url(self):
        return reverse('store:category-list', args=[self.slug])
    
    def __str__(self):
        return self.name 


class ProductType(models.Model):
    """
    ProductType Table will be provide a list of the different
    types of products that are for sale.
    """
    name = models.CharField(
        verbose_name=_('Product Name'),
        max_length=255,
        unique=True,
        help_text=_('Unique'),
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    ProductSpecification Trable contains specification 
    or features for the product types
    """
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.RESTRICT,
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
        help_text=_('Required'),
    )

    class Meta:
        verbose_name = _('Product Specification')
        verbose_name_plural = _('Product Specifications')
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product table contain all the items.
    """
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.RESTRICT,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        help_text=_('Required'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
        help_text=('Not Required'),
        blank=True,
    )
    slug = models.SlugField(max_length=255)
    regular_price=models.DecimalField(
        verbose_name=_('Regular price'),
        max_digits=5,
        decimal_places=2,
        help_text=('Maximum 999.99'),
        error_messages={
            'name': {
                'max_length': _('The price must be between 0 and 999.99')
            },
        },
    )
    discount_price=models.DecimalField(
        verbose_name=_('Discount price'),
        max_digits=5,
        decimal_places=2,
        help_text=('Maximum 999.99'),
        error_messages={
            'name': {
                'max_length': _('The price must be between 0 and 999.99')
            },
        },
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        _('Created at'), 
        auto_now_add=True, 
        editable=False
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        # ordering = ('-created',)
    
    def get_absolute_url(self):
        return reverse('store:product-detail', args=[self.slug])

    def __str__(self):
        return self.title


    
class ProductSpecificationValue(models.Model):
    """
    This table contain each of the product individual 
    specifiation or features.
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE
    )
    specification = models.ForeignKey(
        ProductSpecification, 
        on_delete=models.RESTRICT
    )
    value = models.CharField(
        verbose_name=_('Value'),
        max_length=255,
        help_text=_('Product Specification value (maximum 255 char)'),
    )

    class Meta:
        verbose_name = _('Product Specification Value')
        verbose_name_plural = _('Product Specification Values')
    

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    Product Image table.
    """

    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='product_image'
    )
    image = models.ImageField(
        verbose_name=_('Image'),
        upload_to='images/%Y/%m/%d', 
        default='images/default.png',
        help_text=_('Upload a product image'),
    )
    alt_text = models.CharField(
        verbose_name=_('Alt text'),
        help_text=_('Please add alternative text'),
        max_length=255,
        null=True,
        blank=True
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_ap = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
    

