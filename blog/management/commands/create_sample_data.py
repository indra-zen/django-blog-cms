from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Post, Comment
from django.utils import timezone
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Creates sample data for the blog"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating sample data...")

        # Create users
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f"Created admin user: admin/admin123"))

        author_user, created = User.objects.get_or_create(
            username="author", defaults={"email": "author@example.com"}
        )
        if created:
            author_user.set_password("author123")
            author_user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Created author user: author/author123")
            )

        # Create categories
        categories_data = [
            ("Technology", "Latest tech news and tutorials"),
            ("Programming", "Coding tips and best practices"),
            ("Web Development", "Frontend and backend development"),
            ("Data Science", "Machine learning and data analysis"),
        ]

        categories = []
        for name, description in categories_data:
            category, created = Category.objects.get_or_create(
                name=name, defaults={"description": description}
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))

        # Create posts
        posts_data = [
            {
                "title": "Getting Started with Django",
                "content": """Django is a high-level Python web framework that encourages rapid development 
                and clean, pragmatic design. Built by experienced developers, it takes care of much of the 
                hassle of web development, so you can focus on writing your app without needing to reinvent 
                the wheel. It's free and open source.
                
                In this post, we'll explore the basics of Django and how to get started with your first project.
                Django follows the Model-View-Template (MVT) architectural pattern, which is similar to MVC.
                
                Key features of Django include:
                - ORM (Object-Relational Mapping)
                - Admin interface
                - Authentication system
                - URL routing
                - Template engine
                - Form handling
                
                Let's dive into each of these features and see how they make web development easier!""",
                "excerpt": "Learn the basics of Django and start building powerful web applications.",
                "category": categories[1],
                "author": author_user,
            },
            {
                "title": "Python Best Practices for 2025",
                "content": """Python continues to be one of the most popular programming languages in 2025. 
                Here are some best practices every Python developer should follow:
                
                1. Use virtual environments for every project
                2. Write docstrings for all public modules, functions, classes, and methods
                3. Follow PEP 8 style guide
                4. Use type hints to improve code clarity
                5. Write unit tests for your code
                6. Use meaningful variable names
                7. Keep functions small and focused
                8. Use context managers for resource management
                
                Following these practices will make your code more maintainable and professional.""",
                "excerpt": "Essential Python coding practices every developer should know.",
                "category": categories[1],
                "author": author_user,
            },
            {
                "title": "Building Modern Web Applications",
                "content": """Modern web applications require careful planning and the right technology stack.
                In this comprehensive guide, we'll explore the essential components of modern web development.
                
                Frontend Technologies:
                - HTML5, CSS3, JavaScript
                - React, Vue, or Angular
                - Responsive design principles
                - Progressive Web Apps (PWA)
                
                Backend Technologies:
                - Node.js, Python, Ruby, or PHP
                - RESTful APIs or GraphQL
                - Database design (SQL and NoSQL)
                - Authentication and authorization
                
                DevOps and Deployment:
                - Version control with Git
                - CI/CD pipelines
                - Cloud platforms (AWS, Azure, GCP)
                - Containerization with Docker
                
                Start building amazing web applications today!""",
                "excerpt": "A comprehensive guide to modern web development technologies and practices.",
                "category": categories[2],
                "author": admin_user,
            },
            {
                "title": "Introduction to Machine Learning",
                "content": """Machine Learning is transforming the way we interact with technology.
                From recommendation systems to autonomous vehicles, ML is everywhere.
                
                What is Machine Learning?
                Machine Learning is a subset of artificial intelligence that enables systems to learn
                and improve from experience without being explicitly programmed.
                
                Types of Machine Learning:
                1. Supervised Learning - Learning from labeled data
                2. Unsupervised Learning - Finding patterns in unlabeled data
                3. Reinforcement Learning - Learning through trial and error
                
                Popular ML Libraries:
                - Scikit-learn for traditional ML algorithms
                - TensorFlow and PyTorch for deep learning
                - Pandas and NumPy for data manipulation
                - Matplotlib and Seaborn for visualization
                
                Getting started with ML is easier than ever. Start your journey today!""",
                "excerpt": "Understanding the fundamentals of Machine Learning and AI.",
                "category": categories[3],
                "author": admin_user,
            },
            {
                "title": "The Future of Web Development",
                "content": """Web development is constantly evolving. Let's explore what the future holds.
                
                Emerging Trends:
                - WebAssembly for high-performance web apps
                - JAMstack architecture
                - Serverless computing
                - Edge computing
                - Web3 and decentralized applications
                
                Skills to Learn:
                - TypeScript for type-safe JavaScript
                - Modern CSS (Grid, Flexbox, Custom Properties)
                - Web Components
                - API design and documentation
                - Security best practices
                
                The web platform continues to grow more powerful. Stay ahead of the curve!""",
                "excerpt": "Exploring emerging trends and technologies in web development.",
                "category": categories[2],
                "author": author_user,
            },
        ]

        for post_data in posts_data:
            post, created = Post.objects.get_or_create(
                title=post_data["title"],
                defaults={
                    "content": post_data["content"],
                    "excerpt": post_data["excerpt"],
                    "category": post_data["category"],
                    "author": post_data["author"],
                    "status": "published",
                    "published_at": timezone.now(),
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created post: {post.title}"))

                # Add some comments to each post
                for i in range(2):
                    Comment.objects.create(
                        post=post,
                        author=admin_user if i == 0 else author_user,
                        content=f"Great article! This is very informative and well-written. Thanks for sharing!",
                        approved=True,
                    )

        self.stdout.write(self.style.SUCCESS("Sample data created successfully!"))
