# Import necessary modules
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, MenuItem
from django.core.files.uploadedfile import SimpleUploadedFile

# Define your test class
class CafeViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Test Category', slug='test-category')

        # Create a SimpleUploadedFile to associate with the image attribute
        image_file = SimpleUploadedFile(
            "test_image.png",
            b"file_content",
            content_type="image/png"
        )

        # Create a MenuItem object with an associated image file
        self.menu_item = MenuItem.objects.create(
            name='Test Item',
            slug='test-item',
            category=self.category,
            price=10.0,
            image=image_file  # Associate the image file with the image attribute
        )

    def test_menu_item_view(self):
        url = reverse('menu-item', kwargs={'slug': 'test-item'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/menu_item.html')

    # Test menu item view
    def test_menu_item_view(self):
        url = reverse('menu-item', kwargs={'slug': 'test-item'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/menu_item.html')

    # Test home view
    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/home.html')
        
    # Test Login user view
    def test_login_user_view(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/login.html')
        
    # Test register user view
    def test_register_user_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/register.html')
    
    # Test update user profile view
    def test_update_user_view(self):
        url = reverse('update-user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    

