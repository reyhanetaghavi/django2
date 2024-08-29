from django.contrib import admin
from .models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','phone_number',)  # نمایش فیلدهای مشخص در لیست
    search_fields = ('username','phone_number',)  # قابلیت جستجو

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'family_name', 'gender')  # نمایش فیلدهای مشخص در لیست
    search_fields = ('username' , 'name', 'family_name')  # قابلیت جستجو

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
