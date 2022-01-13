from django.contrib import admin
from .models import User, District, CarDealer, Car, Customer

# Register your models here.
admin.site.register(User)
admin.site.register(District)
admin.site.register(CarDealer)
admin.site.register(Car)
admin.site.register(Customer)

