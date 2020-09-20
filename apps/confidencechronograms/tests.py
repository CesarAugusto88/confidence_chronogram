from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Funcionario

class Status_Code_Tests(TestCase):
    def test_status_code_login(self):
        response = self.client.get(reverse('login_user'))
        self.assertEqual(response.status_code, 200)
    
    def test_status_code_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_status_code_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)