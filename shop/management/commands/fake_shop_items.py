from faker import Faker
from faker.providers import internet, date_time, lorem
from django.core.management.base import BaseCommand
from shop.models import Product, Category
from random import randint, randrange
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify



class Command(BaseCommand):
    def clear_data(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
    def handle(self, *args, **options):
        self.clear_data()
        def set_faker():
            fake = Faker()
            fake.add_provider(internet)
            fake.add_provider(date_time)
            fake.add_provider(lorem)
            return fake
        categories=set_faker().words(nb=15, ext_word_list=None, unique=True)
        for _ in range(0,90):
            fake = set_faker()
            name = fake.word(ext_word_list=categories)
            Category.objects.get_or_create(
                name=name,
                slug=slugify(name)
            )
        for _ in range(0,30):
            fake = set_faker()
            random = randint(0, 30)
            name = fake.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None)
            product, sth = Product.objects.get_or_create(
                name=name,
                slug=slugify(name),
                category=Category.objects.all()[randint(0,len(Category.objects.all())-1)],
                price=random+random/100,
                description=fake.text(max_nb_chars=8000),
                create_date=fake.date_time(),
                start_date=timezone.now()+timedelta(days=random),
                image='mock/{}.jpeg'.format(randrange(1, 15))
            )

print('Data filled in successfully')