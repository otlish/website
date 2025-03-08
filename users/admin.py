from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django import forms

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

class CutomUserAdmin(UserAdmin):
    #admin ma k dekhaune
    form = CustomUserChangeForm
    list_display=('username','email','first_name','last_name','is_staff')
    list_filter=('is_staff','is_active','is_superuser')

    #fields to search by
    search_fields=('username','email','first_name','last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    ordering=('username',)

    actions=['activate_users','deactivate_users']

    def activate_users(self,request,queryset):
        queryset.update(is_active=True)
    activate_users.short_description="Activate selected users"    

    def deactivate_users(self, request, queryset):
      queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"




admin.site.register(CustomUser,CutomUserAdmin)