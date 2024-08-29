from django.db import models
from Users_app.models import *
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='',blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='food_images/')

    class Meta:
        abstract = True


class Appetizer(Food):

    def __str__(self):
        return self.name

class Salad(Food):

    def __str__(self):
        return self.name

class Pizza(Food):

    def __str__(self):
        return self.name

class Burger(Food):

    def __str__(self):
        return self.name

class Pasta(Food):

    def __str__(self):
        return self.name

class Drink(Food):

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def get_total_price(self):
        total_price = 0
        for item in self.items.all():
            if item.pizza:
                total_price += item.pizza.price * item.quantity
            elif item.burger:
                total_price += item.burger.price * item.quantity
            elif item.pasta:
                total_price += item.pasta.price * item.quantity
            elif item.salad:
                total_price += item.salad.price * item.quantity
            elif item.appetizer:
                total_price += item.appetizer.price * item.quantity
            elif item.drink:
                total_price += item.drink.price * item.quantity
        return total_price

    def __str__(self):
        return f"سبد خرید {self.user.username}"
        

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, null=True, blank=True, on_delete=models.CASCADE)
    burger = models.ForeignKey(Burger, null=True, blank=True, on_delete=models.CASCADE)
    pasta = models.ForeignKey(Pasta, null=True, blank=True, on_delete=models.CASCADE)
    salad = models.ForeignKey(Salad, null=True, blank=True, on_delete=models.CASCADE)
    appetizer = models.ForeignKey(Appetizer, null=True, blank=True, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.pizza:
            return f"{self.quantity} x {self.pizza.name}"
        elif self.burger:
            return f"{self.quantity} x {self.burger.name}"
        elif self.pasta:
            return f"{self.quantity} x {self.pasta.name}"
        elif self.salad:
            return f"{self.quantity} x {self.salad.name}"
        elif self.appetizer:
            return f"{self.quantity} x {self.appetizer.name}"
        elif self.drink:
            return f"{self.quantity} x {self.drink.name}"
        return "Item"



class OrderFood(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = [
        ('pending', 'در حال بررسی'),
        ('confirmed', 'تایید شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'تحویل شده'),
        ('canceled', 'لغو شده'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.get_status_display()}"



class OrderItem(models.Model):
    order = models.ForeignKey(OrderFood, on_delete=models.CASCADE, related_name='items')
    pizza = models.ForeignKey(Pizza, null=True, blank=True, on_delete=models.SET_NULL)
    burger = models.ForeignKey(Burger, null=True, blank=True, on_delete=models.SET_NULL)
    pasta = models.ForeignKey(Pasta, null=True, blank=True, on_delete=models.SET_NULL)
    salad = models.ForeignKey(Salad, null=True, blank=True, on_delete=models.SET_NULL)
    appetizer = models.ForeignKey(Appetizer, null=True, blank=True, on_delete=models.SET_NULL)
    drink = models.ForeignKey(Drink, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.pizza or self.burger or self.pasta or self.salad or self.appetizer or self.drink}"
