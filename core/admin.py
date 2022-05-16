from django.contrib import admin
from .models import Profile, Post, PlacedOrder, Comment

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
class PlacedOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_no','products',)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PlacedOrder, PlacedOrderAdmin)
admin.site.register(Comment, CommentAdmin)
