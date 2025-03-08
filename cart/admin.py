from django.contrib import admin
from .models import CartItem

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'quantity', 'size',   'user','image' )  # Fields to display in the list
    list_filter = ('user', 'size')  # Optional filters
    search_fields = ('product_name', 'user__username', 'user__email')  # Fields to search by
    ordering = ('user', 'product_name')  # Default ordering
    actions = ['update_quantity']

    # Optionally, customize the form view
    # fieldsets = (
    #     (None, {'fields': ('user', 'product_name', 'price', 'quantity', 'size' ,'image')}),
    #     ('Total Price', {'fields': ('total_price',)}),
    # )

    def update_quantity(self, request, queryset):
        # Custom action to update quantity (example)
        queryset.update(quantity=1)  # This is just an example. Adjust as needed.
    update_quantity.short_description = 'Reset quantity to 1 for selected cart items'

admin.site.register(CartItem, CartItemAdmin)
