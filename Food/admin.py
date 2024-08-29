from django.contrib import admin
from .models import Pizza, Burger, Pasta, Drink, Appetizer, Salad, CartItem,Cart

admin.site.register(Appetizer)
admin.site.register(Salad)
admin.site.register(Pizza)
admin.site.register(Burger)
admin.site.register(Pasta)
admin.site.register(Drink)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_price']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'get_item_name', 'quantity']

    def get_item_name(self, obj):
        if obj.pizza:
            return obj.pizza.name
        elif obj.burger:
            return obj.burger.name
        elif obj.pasta:
            return obj.pasta.name
        elif obj.salad:
            return obj.salad.name
        elif obj.appetizer:
            return obj.appetizer.name
        elif obj.drink:
            return obj.drink.name
        return "Item"

    get_item_name.short_description = 'Item Name'


from .models import OrderFood, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(OrderFood)
class OrderFoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'status')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at') 
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'pizza', 'burger', 'pasta', 'salad', 'appetizer', 'drink', 'quantity')
    list_filter = ('order', 'pizza', 'burger', 'pasta', 'salad', 'appetizer', 'drink')


    #this is a comment for test :)