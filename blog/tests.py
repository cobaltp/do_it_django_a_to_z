from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 1.1. Load post list page.
        response = self.client.get('/blog/')
        # 1.2. Check if page loaded properly.
        self.assertEqual(response.status_code, 200)
        # 1.3. Check page title.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # 1.4. Check if there is a navigation bar.
        navbar = soup.nav
        # 1.5. Check if there are certain texts in navbar.
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # 2.1. If there are no posts in page,
        self.assertEqual(Post.objects.count(), 0)
        # 2.2. Show some message something like "there are no posts in this page".
        main_area = soup.find('div', id='main-area')
        self.assertIn('There are no posts yet.', main_area.text)

        # 3.1. If there is two posts,
        post_001 = Post.objects.create(
            title='first post',
            content='first content',
        )
        post_002 = Post.objects.create(
            title='second post',
            content='second content',
        )
        self.assertEqual(Post.objects.count(), 2)
        # 3.2. Refresh page and check if the page loaded properly.
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 3.3. Check if there are title of two posts that we created before.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4. Check if there is no "there are no posts in this page".
        self.assertNotIn('There are no posts yet.', main_area.text)

    def test_post_detail(self):
        # 1.1. Create single post.
        post_001 = Post.objects.create(
            title='first post',
            content='first content',
        )
        # 1.2. Check post url.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 2.1. Check if the first post loaded properly.
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup =  BeautifulSoup(response.content, 'html.parser')
        # 2.2. Check there is a navigation bar.
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)
        # 2.3. Check if the page has a proper title.
        self.assertIn(post_001.title, soup.title.text)
        # 2.4. Check if the title is located at div 'post-area'
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        # 2.5. Check there is a author in div 'post-area'
        # 2.6. Check there is a content in div 'post-area'
        self.assertIn(post_area.content, post_area.text)