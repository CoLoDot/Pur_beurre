from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Users, Products, Saving
from .form import Connexion
from substitut.cron.update import update as updating_products_table

# Create your tests here.

class PageTestCase(TestCase):

    def test_index_page(self):
        """Test if Index Page return status code 200"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_mentionlegales_page(self):
        """Test if Mention Légales Page return status code 200"""
        response = self.client.get(reverse('substitut:mentionslegales'))
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        """Test if Search Page return status code 200"""
        response = self.client.get(reverse('substitut:search'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        """Test if SignUp Page return status code 200"""
        response = self.client.get(reverse('substitut:signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """Test if Login Page return status code 200"""
        response = self.client.get(reverse('substitut:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        """Test if Logout Page return status code 200"""
        response = self.client.get(reverse('substitut:logout'))
        self.assertEqual(response.status_code, 200)

    def test_user_account_page(self):
        """Test if User Account Page return status code 200"""
        response = self.client.get(reverse('substitut:useraccount'))
        self.assertEqual(response.status_code, 200)

    def test_user_products_page(self):
        """Test if User Products Page return status code 200"""
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
        """Test if Detail Page return status code 200"""
        product_id = self.product.id
        response = self.client.get(reverse('substitut:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        """Test if Detail Page return status code 404"""
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
        """Test if Form is valid"""
        form = Connexion(data={'username': 'Coco',
                               'email': self.contact.email,
                               'password': self.contact.password})
        self.assertTrue(form.is_valid())

    def test_form_not_valid(self):
        """Test if Form is not valid"""
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
        """Test if a User is logged in"""
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('substitut:login'))
        self.assertEqual(login, True)
        self.assertEqual(str(response.context['user']), self.username)

    def test_user_logout(self):
        """Test if a User is logged Out"""
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
                                category=['coco', 'cococho'],
                                url='http://chocolatchaud',
                                picture='http://chocolatchaudpicture')
        self.product = Products.objects.get(name='Chocolat Chaud')

    def test_saving_product_is_registered(self):
        """Test if a product is saved in user's DB"""
        product_id = self.product.id
        save_to_db = Saving.objects.create(contact=self.contact.email,
                                           product_key=self.product.id)
        self.assertEqual(product_id, save_to_db.product_key)

    def test_saving_product_not_registered(self):
        """Test if a product is not saved in user's DB"""
        product_id = self.product.id
        save_to_db = Saving.objects.create(contact=self.contact.email,
                                           product_key=product_id + 1)
        self.assertNotEqual(product_id, save_to_db.product_key)


class CronTestCase(TestCase):

    def setUp(self):
        Products.objects.create(name='Chocolat Chaud',
                                nutriscore='d',
                                category=['coco', 'cococho'],
                                url='http://chocolatchaud',
                                picture='http://chocolatchaudpicture')
        Products.objects.create(name='Chocolat Noir',
                                nutriscore='d',
                                category=['coco', 'cococho'],
                                url='http://chocolatchaud',
                                picture='http://chocolatchaudpicture')

    def test_update_products_model(self):
        get_product_db_len = len(Products.objects.all())
        updating_products_table()
        get_product_db_len_after_update = len(Products.objects.all())
        self.assertGreater(get_product_db_len_after_update, get_product_db_len)