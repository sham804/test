from django.contrib import admin
from my_work.models import CustomUser,Profile

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Profile)