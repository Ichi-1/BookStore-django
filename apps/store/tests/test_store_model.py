from urllib import response
import pytest
from django.urls import reverse


def test_category_str(product_category):
    assert product_category.__str__() == 'django'


def test_category_reverse(client, product_category):
    category = product_category
    url = reverse('store:category-list', kwargs={'category_slug': category})
    response = client.get(url)
    assert response.status_code == 200


def test_product_type_str(product_type):
    assert product_type.__str__() == 'book'


def test_product_spec_str(product_specification):
    assert product_specification.__str__() == 'Author'


def test_product_str(product):
    assert product.__str__() == 'product_title'


# def test_product_url_reverse(client, product):
#     slug = 'product_slug'
#     category_slug = product.category.slug

#     url = reverse('store:product-detail', kwargs={'category_slug':category_slug, 'slug': slug}) 
#     response = client.get(url)

#     assert response.status_code == 200


def test_product_specification_value(product_specification_value):
    assert product_specification_value.__str__() == '100'