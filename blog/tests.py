from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from .models import Post, Comment, Category, Tag

# Create your tests here.
def test_navbar(tv: TestCase, soup: BeautifulSoup):
    # 1.1. Check if there is a navigation bar.
    navbar = soup.nav
    # 1.2. Check if there are certain texts in navbar.
    tv.assertIn('Blog', navbar.text)
    tv.assertIn('About Me', navbar.text)

    logo_button = navbar.find('a', text='Navbar')
    tv.assertIn(logo_button.attrs['href'], '/')

    home_button = navbar.find('a', text='Navbar')
    tv.assertIn(home_button.attrs['href'], '/')

    blog_button = navbar.find('a', text='Navbar')
    tv.assertIn(blog_button.attrs['href'], '/blog/')

    about_me_button = navbar.find('a', text='Navbar')
    tv.assertIn(about_me_button.attrs['href'], '/about_me/')

def test_category_card(tv: TestCase, soup: BeautifulSoup):
    # 1.1. Check if there is a categories card.
    categories_card = soup.find('div', id='categories-card')
    # 1.2. Check if there are certain texts in card.
    tv.assertIn('Categories', categories_card.text)
    tv.assertIn(f'{tv.category_programming.name} ({tv.category_programming.post_set.count()})', categories_card.text)
    tv.assertIn(f'{tv.category_music.name} ({tv.category_music.post_set.count()})', categories_card.text)
    tv.assertIn(f'No category (1)', categories_card.text)

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_001 = User.objects.create_user(
            username='user001',
            password='testpsword000',
        )
        self.user_002 = User.objects.create_user(
            username='user002',
            password='testpsword000',
        )
        self.user_002.is_staff = True
        self.user_002.save()
        self.category_programming = Category.objects.create(
            name='programming',
            slug='programming',
        )
        self.category_music = Category.objects.create(
            name='music',
            slug='music',
        )
        self.tag_python = Tag.objects.create(
            name='python00',
            slug='python00',
        )
        self.tag_python_2 = Tag.objects.create(
            name='python02',
            slug='python02',
        )
        self.tag_hello = Tag.objects.create(
            name='hello',
            slug='hello',
        )
        self.post_001 = Post.objects.create(
            title='first post',
            content='first content',
            category=self.category_programming,
            author=self.user_001,
        )
        self.post_001.tags.add(self.tag_hello)
        self.post_002 = Post.objects.create(
            title='second post',
            content='second content',
            category=self.category_music,
            author=self.user_002,
        )
        self.post_003 = Post.objects.create(
            title='third post',
            content='third content',
            author=self.user_002,
        )
        self.post_003.tags.add(self.tag_python)
        self.post_003.tags.add(self.tag_python_2)
        self.comment_001 = Comment.objects.create(
            post=self.post_001,
            author=self.user_001,
            content='first comment',
        )

    def test_post_list(self):
        # 1. If there is 3 posts,
        self.assertEqual(Post.objects.count(), 3)
        # 1.1. Load post list page and check if the page loaded properly.
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 1.2. Check if there is no "there are no posts in this page".
        main_area = soup.find('div', id='main-area')
        self.assertNotIn('There are no posts yet.', main_area.text)
        # 1.3. Check navbar and categories card.
        test_navbar(self, soup)
        test_category_card(self, soup)
        # 1.4. Check the first post.
        post_001_card = soup.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_2.name, post_001_card.text)
        # 1.5. Check the second post.
        post_002_card = soup.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_2.name, post_002_card.text)
        # 1.6. Check the third post.
        post_003_card = soup.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('No category', post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_2.name, post_003_card.text)
        # 1.7. Check if there is author name in posts.
        self.assertIn(self.user_001.username, main_area.text)
        self.assertIn(self.user_002.username, main_area.text)

        # 2. If there is no posts,
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        # 2.1. Load post list page and check if the page loaded properly.
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 2.2. Show some message something like "there are no posts in this page".
        main_area = soup.find('div', id='main-area')
        self.assertIn('There are no posts yet.', main_area.text)

    def test_post_detail(self):
        # 1.1. Check post url.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')
        # 1.2. Check if the post loaded properly.
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 2.2. Check navbar and categories card.
        test_navbar(self, soup)
        test_category_card(self, soup)
        # 2.3. Check if the page has a proper title.
        self.assertIn(self.post_001.title, soup.title.text)
        # 2.4. Check if the title and category badge are located properly.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('article', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.post_001.category.name, post_area.text)
        # 2.5. Check there is a author in div 'post-area'
        self.assertIn(self.user_001.username, post_area.text)
        # 2.6. Check there is a content in div 'post-area'
        self.assertIn(self.post_001.content, post_area.text)
        # 2.7. Check if there are some tags.
        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_2.name, post_area.text)
        # 2.8. Check comments
        comment_area = soup.find('section', id='comment-area')
        comment_001_area = comment_area.find('div', id='comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)

    def test_comment_form(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('section', id='comment-area')
        self.assertIn('Login and leave a comment!', comment_area.text)
        self.assertFalse(comment_area.find('form', id='comment-form'))

        self.client.login(username='user001', password='testpsword000')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('section', id='comment-area')
        self.assertNotIn('Login and leave a comment!', comment_area.text)
        comment_form = comment_area.find('form', id='comment-form')
        self.assertTrue(comment_form.find('textarea', id='id_content'))
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content': 'new comment',
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)

        new_comment = Comment.objects.last()

        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)

        comment_area = soup.find('section', id='comment-area')
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        self.assertIn('user001', new_comment_div.text)
        self.assertIn('new comment', new_comment_div.text)

    def test_comment_update(self):
        comment_test_002= Comment.objects.create(
            post=self.post_001,
            author=self.user_002,
            content='comment by 002',
        )

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('section', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

        self.client.login(username='user001', password='testpsword000')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('section', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))
        comment_001_update_btn = comment_area.find('a', id='comment-1-update-btn')
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')

        response = self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Comment - Blog', soup.title.text)
        update_comment_form = soup.find('form', id='comment-form')
        content_textarea = update_comment_form.find('textarea', id='id_content')
        self.assertIn(self.comment_001.content, content_textarea.text)

        response = self.client.post(
            f'/blog/update_comment/{self.comment_001.pk}/',
            {
                'content': 'edit first comment',
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_001_div = soup.find('div', id='comment-1')
        self.assertIn('edit first comment', comment_001_div.text)
        self.assertIn('Updated: ', comment_001_div.text)

    def test_delete_comment(self):
        comment_test_002 = Comment.objects.create(
            post=self.post_001,
            author=self.user_002,
            content='comment by 002',
        )

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('section', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-delete-modal-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-delete-modal-btn'))

        self.client.login(username='user002', password='testpsword000')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('section', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-delete-modal-btn'))
        comment_002_delete_modal_btn = comment_area.find('a', id='comment-2-delete-modal-btn')
        self.assertIn('delete', comment_002_delete_modal_btn.text)

        delete_comment_modal_002 = soup.find('div', id='deleteCommentModal-2')
        self.assertIn('Are You Sure?', delete_comment_modal_002.text)
        really_delete_btn_002 = delete_comment_modal_002.find('a')
        self.assertIn('Delete', really_delete_btn_002.text)
        self.assertEqual(
            really_delete_btn_002.attrs['href'],
            '/blog/delete_comment/2/',
        )

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        response = self.client.get('/blog/delete_comment/2/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertIn(self.post_001.title, soup.title.text)
        comment_area = soup.find('section', id='comment-area')
        self.assertNotIn('comment by 002', comment_area.text)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)

    def test_category_page(self):
        # 1. Check if category page loaded properly.
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 2. Check navbar and categories card.
        test_navbar(self, soup)
        test_category_card(self, soup)
        # 3. Check if there is category badge in the area.
        self.assertIn(self.category_programming.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_tag_page(self):
        # 1. Check if tag page loaded properly.
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 2. Check navbar and categories card.
        test_navbar(self, soup)
        test_category_card(self, soup)
        # 3. Check if there is tag badge in the area.
        self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_create_page(self):
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='user001', password='testpsword000')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='user002', password='testpsword000')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)

        self.client.post(
            '/blog/create_post/',
            {
                'title': 'test create post',
                'content': 'test create post content',
                'tags_str': 'new tag; test, python00',
            }
        )
        self.assertEqual(Post.objects.count(), 4)
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, 'test create post')
        self.assertEqual(last_post.author.username, 'user002')

        self.assertEqual(last_post.tags.count(), 3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='test'))
        self.assertEqual(Tag.objects.count(), 5)

    def test_update_page(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        self.assertNotEqual(self.post_003.author, self.user_001)
        self.client.login(username=self.user_001.username, password='testpsword000')
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='user002', password='testpsword000')
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('python00; python02', tag_str_input.attrs['value'])

        self.client.post(
            update_post_url,
            {
                'title': 'third post edit',
                'content': 'third content edit',
                'category': self.category_music.pk,
                'tags_str': 'python test; python02; some tag'
            },
            follow=True
        )
        response = self.client.get(f'/blog/{self.post_003.pk}/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('third post edit', main_area.text)
        self.assertIn('third content edit', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        self.assertIn('python test', main_area.text)
        self.assertIn('python02', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('python00', main_area.text)

    def test_search(self):
        post_test_python = Post.objects.create(
            title='python',
            content='python abcdefghijklmnopqrstuvwxyz',
            author=self.user_001,
        )

        response = self.client.get('/blog/search/python/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')

        self.assertIn('Search: python (2)', main_area.text)
        self.assertNotIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_003.title, main_area.text)
        self.assertIn(post_test_python.title, main_area.text)
