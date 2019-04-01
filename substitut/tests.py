from django.test import TestCase
from django.urls import reverse
from .models import Users, Products, Saving

# Create your tests here.
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)



class DetailPageTestCase(TestCase):

    # test that detail page returns a 200 if the item exists.
    def test_detail_page_returns_200(self):
        Products.objects.create(name="Choco", picture="http://urlchocoimg", nutriscore="c", url="http://urltochoco")
        product_id = Products.objects.get(name="Choco").id
        response = self.client.get(reverse('substitut:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    # test that detail page returns a 404 if the item does not exist.