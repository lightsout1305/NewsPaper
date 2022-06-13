from django.contrib import admin
from .models import Post, Category, PostCategory

admin.register(Post)
admin.register(Category)
admin.register(PostCategory)
# Register your models here.
