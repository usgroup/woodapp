from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)



class CustomUser(AbstractUser):
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    
class Container(Base):
    name = models.CharField(max_length=255, verbose_name="Container nomi")
    come_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.name} | {self.come_date}"
    
    
    
class ProductSize(Base): 
    product_size_x = models.FloatField(verbose_name="Eni")
    product_size_y = models.FloatField(verbose_name="Bo'yi")
    product_size_z = models.FloatField(verbose_name="Balandligi")
    
    def __str__(self) -> str:
        return f"{self.product_size_x} x {self.product_size_y} x {self.product_size_z}"
    
    
class Product(Base): # info product
    product_container = models.ForeignKey(Container, on_delete=models.CASCADE, verbose_name="cointainer nomi", related_name="container_products")
    product_size = models.ForeignKey(ProductSize, on_delete=models.PROTECT, verbose_name="Mahsulot razmeri", related_name="products")
    product_qty = models.IntegerField(verbose_name="Mahsulot soni / dona")
    product_cube = models.FloatField(verbose_name="Mahsulot miqdori / metr kub")
    come_cost = models.IntegerField(verbose_name="Kelgan narxi")
    rest_cube = models.FloatField(blank=True, null=True,verbose_name="Qoldiq miqdori / metr kub")
    rest_qty = models.IntegerField(blank=True, null=True, verbose_name="Qoldiq soni / dona")
    
    
class SaleProduct(Base): #sotilganlar
    product_size = models.ForeignKey(ProductSize, on_delete=models.PROTECT, verbose_name="Mahsulot razmeri")
    selling_price = models.IntegerField(verbose_name="Sotilish narxi")
    amount_sold = models.IntegerField(verbose_name="Sotilgan miqdori | dona")
    

class ExpenseType(Base): # chiqimlar turi
    title = models.CharField(max_length=255, verbose_name="Chiqim turi")
    
    def __str__(self) -> str:
        
        return self.title
    
    
class Worker(Base): # ishchilar
    name = models.CharField(max_length=255, verbose_name="Ismi")
    phone = models.CharField(max_length=13, verbose_name="telefon raqami")
    birth_date = models.DateField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name



class Expense(Base): # chiqimlar
    CURRENCY_TYPE = (
        (1, "USD"),
        (2, "UZS")
    )
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.PROTECT, blank=True, null=True)
    workers = models.ForeignKey(Worker, on_delete=models.PROTECT, blank=True, null=True)
    currency = models.IntegerField(choices=CURRENCY_TYPE, default=1)
    expense_summa = models.IntegerField(verbose_name="xarajat summasi")
    exchange_rate = models.IntegerField(verbose_name="Valyuta kursi")
    expense_distribute = models.ManyToManyField(Container, verbose_name="Containerga chiqim")
    
    def __str__(self) -> str:
        return f"{self.expense_type} | {self.workers} | {self.expense_summa}"

    
    
# class Client(Base): # mijozlar
#     name = models.CharField(max_length=255, verbose_name="Ismi")
#     phone = models.CharField(max_length=13, verbose_name="telefon raqami")
    
#     def __str__(self) -> str:
#         return self.name
    