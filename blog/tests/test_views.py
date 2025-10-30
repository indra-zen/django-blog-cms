from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Category, Post


class HomeViewTest(TestCase):
    """Test home view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")

        # Create published post
        self.post = Post.objects.create(
            title="Published Post",
            content="Content" * 20,
            author=self.user,
            category=self.category,
            status="published",
        )

        # Create draft post
        self.draft = Post.objects.create(
            title="Draft Post",
            content="Content" * 20,
            author=self.user,
            category=self.category,
            status="draft",
        )

    def test_home_view_status_code(self):
        """Test home page loads"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """Test correct template used"""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "blog/home.html")

    def test_home_view_shows_published_posts(self):
        """Test only published posts shown"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "Draft Post")

    def test_home_view_search(self):
        """Test search functionality"""
        response = self.client.get(reverse("home") + "?q=Published")
        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "Draft Post")


class PostDetailViewTest(TestCase):
    """Test post detail view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Test Post",
            content="Content" * 20,
            author=self.user,
            category=self.category,
            status="published",
        )

    def test_post_detail_view(self):
        """Test post detail page loads"""
        response = self.client.get(
            reverse("post_detail", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_post_detail_404(self):
        """Test 404 for non-existent post"""
        response = self.client.get(
            reverse("post_detail", kwargs={"slug": "nonexistent"})
        )
        self.assertEqual(response.status_code, 404)


class CreatePostViewTest(TestCase):
    """Test create post view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")

    def test_create_post_requires_login(self):
        """Test redirect if not logged in"""
        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn("/login/", response.url)

    def test_create_post_logged_in(self):
        """Test create post when logged in"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, 200)

    def test_create_post_submission(self):
        """Test creating a post"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("create_post"),
            {
                "title": "New Post",
                "content": "New content" * 20,
                "category": self.category.id,
                "status": "draft",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Post.objects.filter(title="New Post").exists())


class EditPostViewTest(TestCase):
    """Test edit post view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Test Post",
            content="Content" * 20,
            author=self.user,
            category=self.category,
        )

    def test_edit_own_post(self):
        """Test author can edit own post"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("edit_post", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_cannot_edit_others_post(self):
        """Test user cannot edit others' posts"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(
            reverse("edit_post", kwargs={"slug": self.post.slug})
        )
        # View redirects to post detail with error message
        self.assertEqual(response.status_code, 302)
        self.assertIn("/post/test-post/", response.url)

    def test_staff_can_edit_any_post(self):
        """Test staff can edit any post"""
        staff_user = User.objects.create_user(
            username="staff", password="testpass123", is_staff=True
        )
        self.client.login(username="staff", password="testpass123")
        response = self.client.get(
            reverse("edit_post", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)


class DeletePostViewTest(TestCase):
    """Test delete post view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Test Post",
            content="Content" * 20,
            author=self.user,
            category=self.category,
        )

    def test_delete_post_requires_login(self):
        """Test delete requires login"""
        response = self.client.get(
            reverse("delete_post", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_post_get_shows_confirmation(self):
        """Test GET request shows delete confirmation page"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("delete_post", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/delete_post.html")

    def test_delete_own_post(self):
        """Test author can delete own post"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("delete_post", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(title="Test Post").exists())

    def test_cannot_delete_others_post(self):
        """Test user cannot delete others' posts"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(
            reverse("delete_post", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="Test Post").exists())

    def test_staff_can_delete_any_post(self):
        """Test staff can delete any post"""
        staff_user = User.objects.create_user(
            username="staff", password="testpass123", is_staff=True
        )
        self.client.login(username="staff", password="testpass123")
        response = self.client.post(
            reverse("delete_post", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(title="Test Post").exists())


class CategoryPostsViewTest(TestCase):
    """Test category posts view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Tech Post",
            content="Content" * 20,
            author=self.user,
            category=self.category,
            status="published",
        )

    def test_category_posts_view(self):
        """Test category posts page loads"""
        response = self.client.get(
            reverse("category_posts", kwargs={"slug": self.category.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech Post")

    def test_category_posts_404(self):
        """Test 404 for non-existent category"""
        response = self.client.get(
            reverse("category_posts", kwargs={"slug": "nonexistent"})
        )
        self.assertEqual(response.status_code, 404)


class UserPostsViewTest(TestCase):
    """Test user posts view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="My Post",
            content="Content" * 20,
            author=self.user,
            category=self.category,
        )

    def test_user_posts_requires_login(self):
        """Test user posts requires login"""
        response = self.client.get(reverse("user_posts"))
        self.assertEqual(response.status_code, 302)

    def test_user_posts_view(self):
        """Test user posts page loads"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("user_posts"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Post")


class RegisterViewTest(TestCase):
    """Test register view"""

    def setUp(self):
        self.client = Client()

    def test_register_view_get(self):
        """Test register page loads"""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/register.html")

    def test_register_redirects_if_logged_in(self):
        """Test logged in user redirected from register"""
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 302)

    def test_register_creates_user(self):
        """Test registration creates user"""
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "complexpass123",
                "password2": "complexpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())


class PostDetailCommentTest(TestCase):
    """Test posting comments on post detail"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Test Post",
            content="Content" * 20,
            author=self.user,
            category=self.category,
            status="published",
        )

    def test_add_comment_requires_login(self):
        """Test adding comment requires login"""
        response = self.client.post(
            reverse("post_detail", kwargs={"slug": self.post.slug}),
            {"content": "Test comment"},
        )
        # Should still show the page but not create comment
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.comments.count(), 0)

    def test_add_comment_logged_in(self):
        """Test logged in user can add comment"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("post_detail", kwargs={"slug": self.post.slug}),
            {"content": "Test comment"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.comments.count(), 1)


class HomeViewPaginationTest(TestCase):
    """Test home view pagination"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")

        # Create 15 posts to test pagination
        for i in range(15):
            Post.objects.create(
                title=f"Post {i}",
                content="Content" * 20,
                author=self.user,
                category=self.category,
                status="published",
            )

    def test_pagination(self):
        """Test pagination works"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        # Should show 10 posts per page
        self.assertEqual(len(response.context["page_obj"]), 10)

    def test_pagination_page_2(self):
        """Test second page of pagination"""
        response = self.client.get(reverse("home") + "?page=2")
        self.assertEqual(response.status_code, 200)
        # Should show remaining 5 posts
        self.assertEqual(len(response.context["page_obj"]), 5)


class CreatePostPublishedTest(TestCase):
    """Test creating published posts"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")

    def test_create_published_post_sets_published_at(self):
        """Test creating published post sets published_at"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Published Post",
                "content": "Content" * 20,
                "category": self.category.id,
                "status": "published",
            },
        )
        post = Post.objects.get(title="Published Post")
        self.assertIsNotNone(post.published_at)

    def test_edit_to_published_sets_published_at(self):
        """Test editing draft to published sets published_at"""
        post = Post.objects.create(
            title="Draft Post",
            content="Content" * 20,
            author=self.user,
            category=self.category,
            status="draft",
        )
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("edit_post", kwargs={"slug": post.slug}),
            {
                "title": "Draft Post",
                "content": "Content" * 20,
                "category": self.category.id,
                "status": "published",
            },
        )
        post.refresh_from_db()
        self.assertIsNotNone(post.published_at)


class HomeViewCategoryFilterTest(TestCase):
    """Test filtering by category on home"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.tech_category = Category.objects.create(name="Tech")
        self.science_category = Category.objects.create(name="Science")

        self.tech_post = Post.objects.create(
            title="Tech Post",
            content="Content" * 20,
            author=self.user,
            category=self.tech_category,
            status="published",
        )

        self.science_post = Post.objects.create(
            title="Science Post",
            content="Content" * 20,
            author=self.user,
            category=self.science_category,
            status="published",
        )

    def test_filter_by_category(self):
        """Test filtering posts by category"""
        response = self.client.get(
            reverse("home") + f"?category={self.tech_category.slug}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech Post")
        self.assertNotContains(response, "Science Post")
