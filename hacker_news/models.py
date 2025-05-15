from django.db import models

from django.db import models
from django.utils.timezone import now
from django.utils.timesince import timesince

class Details(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    def __str__(self):
        return self.username
    
class Posts(models.Model):
    user = models.ForeignKey(Details, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    link = models.URLField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    # comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def time_since_posted(self):
        return timesince(self.created_at) + " ago"

    def __str__(self):
        return f"{self.title} by {self.user.username}"
 

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()

    def __str__(self):
        return f"Comment by on {self.post.title}"