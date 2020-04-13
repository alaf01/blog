from django.db import models
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def unpublish(self):
        self.published_date = None
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

#method which tells Django where to go back to after creation of the model
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk':self.pk})

    @property
    def is_published(self):
        return self.published_date != None

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def approve(self):
        self.approved_comment = True
        self.save()

    def disapprove(self):
        self.approved_comment = False
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def get_score_up(self):
        self.score+=1
        self.save()

    def get_score_down(self):
        self.score-=1
        self.save()

    def __str__(self):
        return self.author

class Photo(models.Model):
    post = models.ForeignKey('blog.Post', related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='blogPhotos')
