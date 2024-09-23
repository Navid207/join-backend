from django.contrib import admin
from .models import Contact, Task, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Contact)