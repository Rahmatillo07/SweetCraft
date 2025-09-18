from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_ROLE_CHOICE = (
        ('admin', 'Admin'),
        ('courier', 'Courier'),
        ('client', 'Client')
    )

    username = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICE, default='client')

    REQUIRED_FIELDS = ['phone_number']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.username} ({self.role})"


class Ingredient(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='ingredients')
    name = models.CharField(max_length=50, verbose_name="Nomi")
    extra_price = models.PositiveIntegerField(default=0, verbose_name="Qo‘shimcha narx")
    image = models.ImageField(upload_to='ingredients/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} (+{self.extra_price} ming so'm)"


class Cake(models.Model):
    image = models.ImageField(upload_to='cakes/', verbose_name="Rasmi")
    title = models.CharField(max_length=50, verbose_name="To'rt sarlavhasi")
    description = models.TextField(verbose_name="To'rt uchun ta'rif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Pishirilgan vaqti")
    delivery_date = models.DateField(verbose_name='Yetkazib berish sanasi',default='indiniga')
    base_price = models.PositiveIntegerField(verbose_name="Asosiy narx")
    is_available = models.BooleanField(default=True)
    ingredients = models.ManyToManyField(Ingredient, blank=True, related_name="cakes")

    @property
    def total_price(self):
        return self.base_price + sum(i.extra_price for i in self.ingredients.all())

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = (
        ('on_create', 'tayyorlanmoqda'),
        ('on_delivery', "Yo'lda"),
        ('success', 'topshirildi')
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='client',
        related_name='orders'
    )
    cake = models.ForeignKey(
        Cake,
        on_delete=models.CASCADE,
        verbose_name="To'rt"
    )
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='on_create')
    courier = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deliveries",
        limit_choices_to={'role': 'courier'}
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=True,
        related_name="orders",
        verbose_name="Tanlangan qo‘shimchalar"
    )

    def __str__(self):
        return f"{self.user.username} - {self.cake.title} ({self.status})"

    @property
    def total_price(self):
        return self.cake.base_price + sum(i.extra_price for i in self.ingredients.all())
