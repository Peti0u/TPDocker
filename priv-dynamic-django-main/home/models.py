from django.db import models
from django.utils import timezone
from datetime import datetime


class RefundedChoices(models.TextChoices):
    YES = "YES", "Yes"
    NO = "NO", "No"


class CurrencyChoices(models.TextChoices):
    USD = "USD", "USD"
    EUR = "EUR", "EUR"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=100, default="")
    price = models.IntegerField(blank=True, null=True, default=99)

    def __str__(self):
        return self.name + " / $" + str(self.price)

class Sales(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyerEmail = models.EmailField(blank=True, null=True, default="fake@sales.com")
    purchaseDate = models.DateTimeField(blank=True, null=True, default=timezone.now)
    country = models.TextField(blank=True, null=True, default="USA")
    refunded = models.CharField(
        max_length=20, choices=RefundedChoices.choices, default=RefundedChoices.NO
    )
    currency = models.CharField(
        max_length=10, choices=CurrencyChoices.choices, default=CurrencyChoices.USD
    )
    quantity = models.IntegerField(blank=True, null=True, default=1)

    def __str__(self):
        return (
            str(self.product)
            + " / qty: "
            + str(self.quantity)
            + ", "
            + str(self.purchaseDate)
        )

class Titanic(models.Model):
	id = models.AutoField(primary_key=True)
	PassengerId = models.IntegerField(blank=True, null=True)
	Survived = models.IntegerField(blank=True, null=True)
	Pclass = models.IntegerField(blank=True, null=True)
	Name = models.TextField(blank=True, null=True)
	Sex = models.TextField(blank=True, null=True)
	Age = models.FloatField(blank=True, null=True)
	SibSp = models.IntegerField(blank=True, null=True)
	Parch = models.IntegerField(blank=True, null=True)
	Ticket = models.TextField(blank=True, null=True)
	Fare = models.FloatField(blank=True, null=True)
	Cabin = models.TextField(blank=True, null=True)
	Embarked = models.TextField(blank=True, null=True)
