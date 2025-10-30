from django.test import TestCase
from django.contrib.auth.models import User
from blog.forms import PostForm, CommentForm
from blog.models import Category, Post


class PostFormTest(TestCase):
    """Test PostForm"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")

    def test_post_form_valid_data(self):
        """Test form with valid data"""
        form = PostForm(
            data={
                "title": "Test Post",
                "content": "Test content" * 20,
                "category": self.category.id,
                "status": "draft",
            }
        )
        self.assertTrue(form.is_valid())

    def test_post_form_empty_title(self):
        """Test form with empty title"""
        form = PostForm(
            data={
                "title": "",
                "content": "Test content" * 20,
                "category": self.category.id,
                "status": "draft",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_post_form_short_content(self):
        """Test form accepts any content length (no custom validation)"""
        form = PostForm(
            data={
                "title": "Test",
                "content": "Short",
                "category": self.category.id,
                "status": "draft",
            }
        )
        # Form should be valid - no custom content length validation
        self.assertTrue(form.is_valid())


class CommentFormTest(TestCase):
    """Test CommentForm"""

    def test_comment_form_valid(self):
        """Test form with valid data"""
        form = CommentForm(
            data={
                "content": "Test comment",
            }
        )
        self.assertTrue(form.is_valid())

    def test_comment_form_empty(self):
        """Test form with empty content"""
        form = CommentForm(
            data={
                "content": "",
            }
        )
        self.assertFalse(form.is_valid())
