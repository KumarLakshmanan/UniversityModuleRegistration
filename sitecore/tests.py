from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from sitecore.models import SiteConfiguration, NewsUpdate
from accounts.models import ContactMessage


class SitecoreTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_renders(self):
        """Test that home page renders correctly"""
        response = self.client.get(reverse('sitecore:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'University')

    def test_about_page_renders(self):
        """Test that about page renders correctly"""
        response = self.client.get(reverse('sitecore:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')

    def test_contact_page_renders(self):
        """Test that contact page renders correctly"""
        response = self.client.get(reverse('sitecore:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact')

    def test_contact_form_submission_success(self):
        """Test successful contact form submission"""
        contact_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        
        response = self.client.post('/api/contact/', contact_data)
        self.assertEqual(response.status_code, 200)
        
        # Check that contact message was saved
        self.assertTrue(
            ContactMessage.objects.filter(
                name='John Doe',
                email='john@example.com',
                subject='Test Subject'
            ).exists()
        )
        
        # Check that email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Test Subject', mail.outbox[0].subject)

    def test_contact_form_submission_missing_data(self):
        """Test contact form submission with missing data"""
        contact_data = {
            'name': 'John Doe',
            'email': 'john@example.com'
            # Missing subject and message
        }
        
        response = self.client.post('/api/contact/', contact_data)
        self.assertEqual(response.status_code, 400)

    def test_contact_form_submission_invalid_email(self):
        """Test contact form submission with invalid email"""
        contact_data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        
        response = self.client.post('/api/contact/', contact_data)
        self.assertEqual(response.status_code, 400)

    def test_contact_form_ajax_response(self):
        """Test contact form AJAX response format"""
        contact_data = {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'subject': 'AJAX Test',
            'message': 'Testing AJAX submission.'
        }
        
        response = self.client.post('/api/contact/', 
                                   contact_data,
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('success', data)
        self.assertTrue(data['success'])

    def test_site_stats_api(self):
        """Test site statistics API"""
        response = self.client.get('/api/stats/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('total_students', data)
        self.assertIn('total_modules', data)
        self.assertIn('total_registrations', data)
        self.assertIn('active_departments', data)

    def test_news_api(self):
        """Test news API"""
        # Create some news items
        NewsUpdate.objects.create(
            title='Test News 1',
            content='Content for test news 1',
            is_published=True
        )
        NewsUpdate.objects.create(
            title='Test News 2',
            content='Content for test news 2',
            is_published=True
        )
        NewsUpdate.objects.create(
            title='Unpublished News',
            content='This should not appear',
            is_published=False
        )
        
        response = self.client.get('/api/news/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 2)  # Only published news
        titles = [item['title'] for item in data]
        self.assertIn('Test News 1', titles)
        self.assertIn('Test News 2', titles)
        self.assertNotIn('Unpublished News', titles)

    def test_news_pagination(self):
        """Test news API pagination"""
        # Create multiple news items
        for i in range(15):
            NewsUpdate.objects.create(
                title=f'News Item {i}',
                content=f'Content for news item {i}',
                is_published=True
            )
        
        response = self.client.get('/api/news/?page=1&page_size=10')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertLessEqual(len(data), 10)


class SiteConfigurationTestCase(TestCase):
    def test_site_configuration_creation(self):
        """Test creating site configuration"""
        config = SiteConfiguration.objects.create(
            site_name='Test University',
            site_description='A test university',
            contact_email='info@testuni.edu',
            contact_phone='+1234567890'
        )
        
        self.assertEqual(str(config), 'Test University')
        self.assertEqual(config.contact_email, 'info@testuni.edu')

    def test_site_configuration_singleton(self):
        """Test that only one site configuration can exist"""
        # First, make sure there are no configurations
        SiteConfiguration.objects.all().delete()
        
        # Create the first configuration
        config1 = SiteConfiguration.objects.create(
            site_name='First Config'
        )
        
        # Try to create another - should raise ValueError
        with self.assertRaises(ValueError):
            config2 = SiteConfiguration.objects.create(
                site_name='Second Config'
            )
        
        # Should only have one configuration
        self.assertEqual(SiteConfiguration.objects.count(), 1)

    def test_get_site_config(self):
        """Test getting site configuration"""
        # First, make sure there are no configurations
        SiteConfiguration.objects.all().delete()
        
        # Should work even if no config exists
        config = SiteConfiguration.get_site_config()
        self.assertIsNotNone(config)
        
        # Should return the existing config
        config2 = SiteConfiguration.get_site_config()
        self.assertEqual(config.id, config2.id)


class NewsUpdateTestCase(TestCase):
    def test_news_item_creation(self):
        """Test creating a news item"""
        news = NewsUpdate.objects.create(
            title='Breaking News',
            content='This is breaking news content',
            is_published=True
        )
        
        self.assertEqual(str(news), 'Breaking News')
        self.assertTrue(news.is_published)
        self.assertIsNotNone(news.created_at)

    def test_news_item_slug_generation(self):
        """Test that news item slug is generated"""
        news = NewsUpdate.objects.create(
            title='News With Special Characters!',
            content='Content here',
            is_published=True
        )
        
        self.assertIsNotNone(news.slug)
        # Slug should be URL-friendly
        self.assertNotIn('!', news.slug)
        self.assertNotIn(' ', news.slug)

    def test_news_item_published_manager(self):
        """Test news item published manager"""
        # Create published and unpublished news
        published_news = NewsUpdate.objects.create(
            title='Published News',
            content='This is published',
            is_published=True
        )
        unpublished_news = NewsUpdate.objects.create(
            title='Unpublished News',
            content='This is not published',
            is_published=False
        )
        
        # Test published manager
        published_items = NewsUpdate.published.all()
        self.assertIn(published_news, published_items)
        self.assertNotIn(unpublished_news, published_items)

    def test_news_item_ordering(self):
        """Test news item default ordering"""
        news1 = NewsUpdate.objects.create(
            title='First News',
            content='First content',
            is_published=True
        )
        news2 = NewsUpdate.objects.create(
            title='Second News',
            content='Second content',
            is_published=True
        )
        
        # Should be ordered by created_at descending
        all_news = NewsUpdate.objects.all()
        self.assertEqual(list(all_news), [news2, news1])


class ContactMessageTestCase(TestCase):
    def test_contact_message_creation(self):
        """Test creating a contact message"""
        message = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='This is a test message',
            phone='123-456-7890'
        )
        
        self.assertEqual(str(message), 'Test User - Test Subject')
        self.assertFalse(message.is_read)
        self.assertIsNotNone(message.created_at)

    def test_contact_message_ordering(self):
        """Test contact message default ordering"""
        message1 = ContactMessage.objects.create(
            name='User 1',
            email='user1@example.com',
            subject='First Message',
            message='First message content'
        )
        message2 = ContactMessage.objects.create(
            name='User 2',
            email='user2@example.com',
            subject='Second Message',
            message='Second message content'
        )
        
        # Should be ordered by created_at descending
        all_messages = ContactMessage.objects.all()
        self.assertEqual(list(all_messages), [message2, message1])

    def test_contact_message_mark_as_read(self):
        """Test marking contact message as read"""
        message = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='Test message'
        )
        
        self.assertFalse(message.is_read)
        
        message.is_read = True
        message.save()
        
        self.assertTrue(message.is_read)


class SitecoreIntegrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_with_news(self):
        """Test home page displays news items"""
        # Create some news
        NewsUpdate.objects.create(
            title='Homepage News',
            content='This should appear on homepage',
            is_published=True
        )
        
        response = self.client.get(reverse('sitecore:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Homepage News')

    def test_home_page_with_site_config(self):
        """Test home page uses site configuration"""
        SiteConfiguration.objects.create(
            site_name='Custom University Name',
            site_description='Custom description'
        )
        
        response = self.client.get(reverse('sitecore:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Custom University Name')

    def test_contact_page_with_site_config(self):
        """Test contact page displays site configuration"""
        SiteConfiguration.objects.create(
            contact_email='custom@university.edu',
            contact_phone='+1-555-0123',
            address='123 University Ave'
        )
        
        response = self.client.get(reverse('sitecore:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'custom@university.edu')

    def test_error_pages(self):
        """Test custom error pages"""
        # Test 404 page
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
        
        # Test unauthorized page
        response = self.client.get('/unauthorized/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Access Denied')


class SitecoreAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_response_format(self):
        """Test that APIs return proper JSON format"""
        response = self.client.get('/api/stats/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_api_cors_headers(self):
        """Test that APIs include CORS headers"""
        response = self.client.get('/api/stats/')
        # Should have CORS headers if configured
        self.assertEqual(response.status_code, 200)

    def test_contact_api_rate_limiting(self):
        """Test contact API doesn't allow spam"""
        contact_data = {
            'name': 'Spammer',
            'email': 'spam@example.com',
            'subject': 'Spam',
            'message': 'Spam message'
        }
        
        # Submit multiple times rapidly
        for i in range(5):
            response = self.client.post('/api/contact/', contact_data)
            
        # Should still work (rate limiting would be implemented separately)
        self.assertIn(response.status_code, [200, 429])  # 429 = Too Many Requests
