from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Container)
admin.site.register(ProductSize)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ExpenseType)
admin.site.register(Worker)
admin.site.register(Expense)
admin.site.register(Client)
admin.site.register(ClientAccount)
admin.site.register(Payment)



