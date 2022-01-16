from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User, AbstractUser


# Create your models here.


class User(AbstractUser):
    is_car_dealer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)


class District(models.Model):
    pincode = models.CharField(
        validators=[MinLengthValidator(6), MaxLengthValidator(6)],
        max_length=6,
        unique=True,
    )
    district_name = models.CharField(max_length=40)

    def __str__(self):
        return self.district_name


class CarDealer(models.Model):
    car_dealer_name = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    district = models.ManyToManyField(District)
    wallet = models.IntegerField(default=0)  # kaska w PLN do liczenia

    def __str__(self):
        return str(self.car_dealer_name)


class Car(models.Model):  # Vehicle
    CAR_ENGINES = (
        ("PB", "Benzyna"),
        ("ON", "Diesel"),
        ("LPG", "Gaz"),
        ("EE", "Elektryczny"),
    )
    CAR_CAPACITY = (
        ("2", "2-osobowy"),
        ("3", "3-osobowy"),
        ("4", "4-osobowy"),
        ("5", "5-osobowy"),
        ("9", "9-osobowy"),
    )
    car_name = models.CharField(max_length=20)
    color = models.CharField(max_length=16)
    dealer = models.ForeignKey(
        CarDealer,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="car_dealer",
    )
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True
    )
    capacity = models.CharField(choices=CAR_CAPACITY, max_length=2, default=5)
    is_available = models.BooleanField(default=True)
    engine = models.CharField(choices=CAR_ENGINES, max_length=3, default=0)
    ac = models.BooleanField(default=True)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.car_name


class Customer(models.Model):
    customer_name = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.customer_name)


class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    rent = models.CharField(max_length=8)  # ile PLN do wyświetlania
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    days = models.CharField(max_length=3)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer} zarezerwował/a samochód:{self.car} " \
               f"na {self.days} dni, za {self.rent} PLN"
