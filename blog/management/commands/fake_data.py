from factory.django import DjangoModelFactory
from faker import Faker
from faker.providers import internet, date_time, lorem
import factory
from django.core.management.base import BaseCommand
from blog.models import *
from django.contrib.auth.models import User
from random import randint, shuffle
from django.utils import timezone
from datetime import timedelta


# class AuthorFactory(DjangoModelFactory):
#     class Meta:
#         model = User
#
#     password = factory.PostGenerationMethodCall('set_password', 'asdasdasd')
#     username = fake.name()
#     email = fake.email()

# class PostFactory(DjangoModelFactory):
#     class Meta:
#         model = Post
#     fake = Faker()
#     author = User.objects.all()[0]
#     title = self.fake.sentence()
#     text = self.fake.text()
#     create_date = self.fake.date_time()
#     published_date = self.fake.date_time()
#
#
# class CommentFactory(DjangoModelFactory):
#     class Meta:
#         model = Comment
#
#     fake = Faker()
#     post = Post.objects.all()[0]
#     author = User.objects.all()[0]
#     text = self.fake.text()
#     create_date =  self.fake.date_time()
#     approved_comment = True
tag_list = Faker().words(nb=15, ext_word_list=None, unique=True)
choices=["published", "draft"]
class Command(BaseCommand):
    def clear_data(self):
        Post.objects.all().delete()
        Comment.objects.all().delete()
    def handle(self, *args, **options):
        self.clear_data()
        # # author = AuthorFactory.create_batch(size=10)
        # post = PostFactory.create_batch(size=10)
        # comment = CommentFactory.create_batch(size=30)
        def set_faker():
            fake = Faker()
            fake.add_provider(internet)
            fake.add_provider(date_time)
            fake.add_provider(lorem)
            rand_user=randint(0,len(User.objects.all())-1)
            return fake, rand_user
        for _ in range(0,30):
            num=randint(0, 1)
            fake, rand_user = set_faker()
            random= randint(0, 30)
            shuffle(tag_list)
            no_tags = randint(1, 5)
            tags = tag_list[:no_tags]
            post, sth = Post.objects.get_or_create(
                author=User.objects.all()[rand_user],
                title=fake.sentence(),
                text=fake.text(max_nb_chars=8000),
                create_date=fake.date_time(),
                published_date=timezone.now()+timedelta(days=random),
                status='published'
            )
            for tag in tags:
                post.tags.add(tag)

        for _ in range(0,90):
            fake, rand_user = set_faker()
            Comment.objects.get_or_create(
                post=Post.objects.all()[randint(0,len(Post.objects.all())-1)],
                author=User.objects.all()[rand_user],
                text=fake.text(),
                create_date=fake.date_time(),
                approved_comment = True)


print('Data filled in successfully')