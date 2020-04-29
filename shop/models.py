from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
class Cart(models.Model):
    pass

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    create_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    available = models.BooleanField(default=True)
    promotion = models.BooleanField(default=False)
    promotion_end = models.DateField(blank=True,null=True)
    amount = models.IntegerField(default=1)

    class Meta:
            ordering = ('name',)
            index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def buy(self, no=1):
        self.amount -= no
        if self.amount <= 0:
            self.available = False
    
    def promo(self, amount=None, proc=None):
        if amount:
            self.price -= amount
        elif proc:
            self.price = self.price * (1-proc/100)