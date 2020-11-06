from django.contrib import admin
from .models import *
from . import forms
# Register your models here.


admin.site.register(Customer)
admin.site.register(Fooditem)
admin.site.register(UserFooditem)
admin.site.register(Category)
#Category, Fooditem, , UserFooditem