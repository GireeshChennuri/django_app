from hacker_news.models import Details,Posts,Comments
from django.utils import timezone
def run():
    # Create users
    user1 = Details.objects.create(username="alice", password="alice123")
    user2 = Details.objects.create(username="bob", password="bob123")

    # Create 10 posts (5 by each user)
    posts = [
        Posts.objects.create(user=user1, title="Django 5 Released", link="https://djangoproject.com", likes=15, dislikes=1, created_at=timezone.now()),
        Posts.objects.create(user=user1, title="Python Tips and Tricks", link="https://realpython.com", likes=25, dislikes=0, created_at=timezone.now()),
        Posts.objects.create(user=user1, title="AI in 2025", link="https://openai.com", likes=30, dislikes=2, created_at=timezone.now()),
        Posts.objects.create(user=user1, title="Understanding REST APIs", link="https://restfulapi.net", likes=12, dislikes=3, created_at=timezone.now()),
        Posts.objects.create(user=user1, title="Debugging Django", link="https://testdriven.io", likes=10, dislikes=1, created_at=timezone.now()),
        Posts.objects.create(user=user2, title="Linux Basics", link="https://linux.org", likes=20, dislikes=0, created_at=timezone.now()),
        Posts.objects.create(user=user2, title="Docker Tutorial", link="https://docker.com", likes=22, dislikes=1, created_at=timezone.now()),
        Posts.objects.create(user=user2, title="Intro to Kubernetes", link="https://kubernetes.io", likes=18, dislikes=2, created_at=timezone.now()),
        Posts.objects.create(user=user2, title="Web Security Essentials", link="https://owasp.org", likes=28, dislikes=0, created_at=timezone.now()),
        Posts.objects.create(user=user2, title="Flask vs Django", link="https://towardsdatascience.com", likes=35, dislikes=4, created_at=timezone.now())
    ]

    # Add 2 comments to each post
    comments_text = [
        "Great post, thanks for sharing!",
        "Very informative, I learned a lot.",
    ]

    for post in posts:
        for comment in comments_text:
            Comments.objects.create(post=post, comment=comment)

if __name__ == '__main__':
    run()
    print("Data successfully inserted.")