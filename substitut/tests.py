from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Users, Products, Saving
from .form import Connexion


# Create your tests here.

class PageTestCase(TestCase):

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_mentionlegales_page(self):
        response = self.client.get(reverse('substitut:mentionslegales'))
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        response = self.client.get(reverse('substitut:search'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get(reverse('substitut:signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('substitut:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.client.get(reverse('substitut:logout'))
        self.assertEqual(response.status_code, 200)

    def test_user_account_page(self):
        response = self.client.get(reverse('substitut:useraccount'))
        self.assertEqual(response.status_code, 200)

    def test_user_products_page(self):
        response = self.client.get(reverse('substitut:userproducts'))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):

    def setUp(self):
        Products.objects.create(name="Choco",
                                picture="http://urlchocoimg",
                                nutriscore="c",
                                url="http://urltochoco")
        self.product = Products.objects.get(name="Choco")

    def test_detail_page_returns_200(self):
        product_id = self.product.id
        response = self.client.get(reverse('substitut:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        product_id = self.product.id + 1
        response = self.client.get(reverse('substitut:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 404)


class SignupPageTestCase(TestCase):

    def setUp(self):
        Users.objects.create(email='coco@gmail.com',
                             password='cocopassword')
        self.contact = Users.objects.get(email='coco@gmail.com')

    def test_signup_page_returns_200(self):
        email = self.contact.email
        password = self.contact.password
        response = self.client.post(reverse('substitut:signup'), {
            "email": email,
            "password": password
        })
        self.assertEqual(response.status_code, 200)

    def test_form_is_valid(self):
        form = Connexion(data={'username': 'Coco',
                               'email': self.contact.email,
                               'password': self.contact.password})
        self.assertTrue(form.is_valid())

    def test_form_not_valid(self):
        form = Connexion(data={'username': 'Coco',
                               'email': self.contact.email,
                               'password': None})
        self.assertFalse(form.is_valid())


class LoginLogoutTestCase(TestCase):

    def setUp(self):
        self.username = 'coco'
        self.email = 'coco@mail.com'
        self.password = 'testcoco'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)

    def test_user_login(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('substitut:login'))
        self.assertEqual(login, True)
        self.assertEqual(str(response.context['user']), self.username)

    def test_user_logout(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('substitut:login'))
        user_logged = str(response.context['user'])
        logout = self.client.logout()
        response = self.client.post(reverse('substitut:logout'))
        user_anonymous = str(response.context['user'])
        self.assertNotEqual(user_logged, user_anonymous)


class SavingPageTestCase(TestCase):

    def setUp(self):
        Users.objects.create(email='coco@coco.com',
                             password='testpassword')
        self.contact = Users.objects.get(email='coco@coco.com')
        Products.objects.create(name='Chocolat Chaud',
                                nutriscore='d',
                                url='http://chocolatchaud',
                                picture='http://chocolatchaudpicture')
        self.product = Products.objects.get(name='Chocolat Chaud')

    def test_saving_product_is_registered(self):
        product_id = self.product.id
        save_to_db = Saving.objects.create(contact=self.contact.email,
                                           product_key=self.product.id)
        self.assertEqual(product_id, save_to_db.product_key)

    def test_saving_product_not_registered(self):
        product_id = self.product.id
        save_to_db = Saving.objects.create(contact=self.contact.email,
                                           product_key=product_id + 1)
        self.assertNotEqual(product_id, save_to_db.product_key)
