from django.contrib import admin

from .models import(
    Customer,
    Product,
    Cart,
    OrderPlaced,
    Main_Category,
    Sub_Category,
    Category,
    TOPSALE,
    Wishlist,
)


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','state']
    

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(TOPSALE)
class TopsaleEModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','brand','product_image']    
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']
    
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display= ['id','user','customer','product','quantity','ordered_date','status']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display=['user','product']

class Product_Admin(admin.ModelAdmin):
    list_display = ('title', 'discounted_price', 'Categories')
    list_editable = ('Categories')
    admin.site.register(Main_Category)
    admin.site.register(Category)
    admin.site.register(Sub_Category)


