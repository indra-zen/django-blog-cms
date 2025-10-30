from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Category, Post, Comment


class CategoryModelTest(TestCase):
    """Test Category model"""

    def setUp(self):
        """Run before each test"""
        self.category = Category.objects.create(
            name="Technology", description="Tech posts"
        )

    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, "Technology")
        self.assertEqual(self.category.description, "Tech posts")
        self.assertTrue(isinstance(self.category, Category))

    def test_slug_generation(self):
        """Test slug is auto-generated"""
        self.assertEqual(self.category.slug, "technology")

    def test_slug_uniqueness(self):
        """Test duplicate names need different slugs"""
        # Note: Current implementation doesn't auto-generate unique slugs
        # This test verifies slug uniqueness constraint exists
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Technology")

    def test_str_method(self):
        """Test string representation"""
        self.assertEqual(str(self.category), "Technology")


class PostModelTest(TestCase):
    """Test Post model"""

    def setUp(self):
        """Create test data"""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Test Post",
            content="Test content that is long enough to be valid.",
            author=self.user,
            category=self.category,
            status="published",
        )

    def test_post_creation(self):
        """Test post is created correctly"""
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)

    def test_slug_generation(self):
        """Test slug generated from title"""
        self.assertEqual(self.post.slug, "test-post")

    def test_published_posts(self):
        """Test filtering published posts"""
        draft_post = Post.objects.create(
            title="Draft",
            content="Draft content" * 10,
            author=self.user,
            category=self.category,
            status="draft",
        )
        # Filter published posts manually (no manager exists)
        published = Post.objects.filter(status="published")
        self.assertIn(self.post, published)
        self.assertNotIn(draft_post, published)

    def test_approved_comments(self):
        """Test approved_comments property"""
        # Create approved comment
        Comment.objects.create(
            post=self.post, author=self.user, content="Approved comment", approved=True
        )
        # Create unapproved comment
        Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Unapproved comment",
            approved=False,
        )
        self.assertEqual(self.post.approved_comments.count(), 1)


class CommentModelTest(TestCase):
    """Test Comment model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Test Post",
            content="Content" * 20,
            author=self.user,
            category=self.category,
        )
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, content="Test comment"
        )

    def test_comment_creation(self):
        """Test comment is created correctly"""
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user)
        self.assertFalse(self.comment.approved)  # Default is False

    def test_str_method(self):
        """Test string representation"""
        expected = f"Comment by {self.user.username} on {self.post.title}"
        self.assertEqual(str(self.comment), expected)
