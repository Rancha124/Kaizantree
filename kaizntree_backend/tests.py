from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Tag, Item
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta

class APITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for authentication
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.category = Category.objects.create(name="Test Category")
        cls.tag = Tag.objects.create(name="Test Tag")
        cls.item = Item.objects.create(
            sku="SKU001",
            name="Test Item",
            category=cls.category,
            stock_status=100.0,
            available_stock=50.0
        )
        cls.item.tags.add(cls.tag)
        cls.token, _ = Token.objects.get_or_create(user=cls.user)

    def setUp(self):
        self.client = APIClient()
        self.base_url = reverse('item-list') 


    def test_item_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Assuming this is the only item

    def test_category_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Assuming this is the only category

    def test_tag_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Assuming this is the only tag

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue('token' in response.data)

    def test_login_user(self):
        User.objects.create_user('loginuser', 'loginuser@example.com', 'loginpassword')
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'loginpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_create_item_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('item-list'), {
            'name': 'NewItem',
            'sku': 'SKU002',
            'category': self.category.id,
            'tags': [self.tag.id],
            'stock_status': 10.5,
            'available_stock': 5.0
        })
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_access(self):
        # Attempt to create a new item without authentication
        response = self.client.post(reverse('item-list'), {})
        self.assertEqual(response.status_code, 401)  

    def test_item_list_date_range_filter(self):
        # Assuming `setUpTestData` has created an item, we'll create another item with a specific `created_at` date
        # For demonstration, let's manually set `created_at` to a date that would fall outside a given test range
        old_item = Item.objects.create(
            sku="SKU002",
            name="Old Item",
            category=self.category,
            stock_status=50.0,
            available_stock=25.0,
            created_at=timezone.now() - timedelta(days=365)  # 1 year ago
        )

        old_item.created_at = timezone.now() - timedelta(days=365)  # Set to 1 year ago
        old_item.save(update_fields=['created_at'])
        
        self.client.force_authenticate(user=self.user)
        # Set a date range that includes only the recently created item but not `old_item`
        start_date = (timezone.now() - timedelta(days=30)).date().isoformat()  # 30 days ago
        end_date = timezone.now().date().isoformat()  # today
        
        response = self.client.get(reverse('item-list'), {'start_date': start_date, 'end_date': end_date})
        self.assertEqual(response.status_code, 200)
        
        # Check that the response includes the initial item but not the `old_item`
        self.assertEqual(len(response.data), 1)  # Assuming the initial setup had 1 item
        self.assertNotIn(old_item.id, [item['id'] for item in response.data])
    
    def test_protected_routes(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200, f"Expected 200 OK response for authorized access, got {response.status_code}")

        search_query_url = f"{self.base_url}?search=test"
        response = self.client.get(search_query_url)
        self.assertEqual(response.status_code, 200, f"Expected 200 OK response for authorized access with search query, got {response.status_code}")

    def test_access_protected_route_without_authorization(self):
        # Clear any existing authentication credentials
        self.client.credentials()

        # Attempt to access a protected endpoint without authorization
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 401, "Access without authorization should result in 401 Unauthorized")

        response = self.client.post(self.base_url, {'name': 'Unauthorized Item', 'sku': 'SKU999', 'category': 1, 'stock_status': 100, 'available_stock': 50})
        self.assertEqual(response.status_code, 401, "POST without authorization should result in 401 Unauthorized")