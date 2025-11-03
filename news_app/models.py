from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


# Create your models here.
class News(models.Model):
    # Link each news post to a ChiefEditor (the author)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, #Points to the name of the model Django should treat as the user which is ChiefEditor in this case
        on_delete=models.CASCADE, 
        related_name="news"
    )
    title = models.CharField(max_length=255, unique=True)
    body = models.TextField()
    image = CloudinaryField('image')
    video = CloudinaryField('video', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_news_title')
        ]

    def __str__(self):
        return self.title

