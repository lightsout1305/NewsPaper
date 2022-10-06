from django.contrib import admin
from .models import Post, Category, PostCategory, Comment, Author
from django.core.mail import send_mail
from modeltranslation.admin import TranslationAdmin

from NewsPaper.settings import SERVER_EMAIL


class ShopAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        send_mail(
            subject=f'{obj}',
            message=f'{change}',
            from_email=SERVER_EMAIL,
            recipient_list=[request.user.email, ]
        )


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'register_date', 'content_rating')
    list_filter = ('author', 'categories', 'content_rating')
    search_fields = ('author', 'title', 'categories', 'register_date', 'content_rating')


class PostTranslationAdmin(TranslationAdmin):
    model = Post


class CategoryTranslationAdmin(TranslationAdmin):
    model = Category


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)

# Register your models here.
