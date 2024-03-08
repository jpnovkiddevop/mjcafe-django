from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1, related_name='customer')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    slug = models.SlugField(default='')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
            self.slug = slugify(self.first_name)
            super(Customer, self).save()
            
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='')
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save()
        
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.slug)])
    
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='menu_item',
                                 on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/menu/', null=True, blank=True)
    is_offer = models.BooleanField(default=False)
    selling_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    slug = models.SlugField(default='')
    
    def __str__(self):
        return f"{self.name} {self.category} category"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(MenuItem, self).save()
        
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.slug)])
    
class Order(models.Model):
    order_number = models.AutoField(primary_key=True)
    menu_item = models.ForeignKey(MenuItem, related_name='order', 
                                  on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='order', 
                                 on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    slug = models.SlugField(default='')

    def __str__(self):
        return str(self.order_number)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.order_number)
        super(Order, self).save()
        
    def get_absolute_url(self):
        return reverse('detail', args=([str(self.slug)]))