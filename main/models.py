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
    paid_amount = models.FloatField(default=0, verbose_name="Container balansi", blank=True, null=True)
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return f"{self.name} | {self.come_date} | is_active: {self.is_active}"
    

    @property
    def total_sales_revenue_usd(self):
        calc_sum = 0
    
        for order in self.orders.all():
            calc_sum += order.total_summa            
        return calc_sum
    
    
    
    
      
    
class ProductSize(Base): 
    product_size_title = models.CharField(max_length=255, default='text', verbose_name='Nomi')
    product_size_x = models.FloatField(verbose_name="Eni")
    product_size_y = models.FloatField(verbose_name="Bo'yi")
    product_size_z = models.FloatField(verbose_name="Balandligi")
    
    status = models.BooleanField(default=True, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.product_size_x} x {self.product_size_y} x {self.product_size_z}"
    
    
class Product(Base): # info product
    product_container = models.ForeignKey(Container, on_delete=models.CASCADE, verbose_name="cointainer nomi", related_name="container_products")
    product_size = models.ForeignKey(ProductSize, on_delete=models.PROTECT, verbose_name="Mahsulot razmeri", related_name="products")
    product_qty = models.IntegerField(verbose_name="Mahsulot soni / dona", default=0)
    product_cube = models.FloatField(verbose_name="Mahsulot miqdori / metr kub", default=0)
    come_cost = models.IntegerField(verbose_name="Kelgan narxi", default=0)
    rest_cube = models.FloatField(default=0,verbose_name="Qoldiq miqdori / metr kub")
    rest_qty = models.IntegerField(default=0, verbose_name="Qoldiq soni / dona")
    
    is_cut = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    @property
    def total_product_sum(self):
        return self.come_cost * self.product_cube    # 1 kubasini kelgan narxini umumiy kubasiga ko'paytirilgani
    
   

    
    

class ExpenseType(Base): # chiqimlar turi
    title = models.CharField(max_length=255, verbose_name="Chiqim turi")
    is_active = models.BooleanField(default=True)
    

    
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
    expense_summa = models.FloatField(verbose_name="xarajat summasi")
    exchange_rate = models.IntegerField(verbose_name="Valyuta kursi")
    containers = models.ManyToManyField(Container, verbose_name="Containerga chiqim")
    is_active = models.BooleanField(default=True)
    
        
    @property
    def container_sum(self): 
        if self.currency == 1:
            return self.expense_summa / self.containers.count()
        if self.currency == 2:
            return ((self.expense_summa/self.exchange_rate) / self.containers.count())
    
    @property
    def only_sum(self):
        if self.expense_summa == 0:
            return 0
        else:
            return self.expense_summa / self.containers.count()
        
           

    
    
    def __str__(self) -> str:
        return f"{self.expense_type} | {self.workers} | {self.expense_summa}"

    
    
class Client(Base): # mijozlar
    name = models.CharField(max_length=255, verbose_name="Ismi")
    phone = models.CharField(max_length=13, verbose_name="telefon raqami")
    
    @property
    def debt_usd(self):
        debt_usd = 0
        for c in self.client_account.all():
            debt_usd += c.debt_usd
        return debt_usd
    
    @property
    def debt_uzs(self):
        debt_uzs = 0
        for c in self.client_account.all():
            debt_uzs += c.debt_uzs
        return debt_uzs
    
    def __str__(self) -> str:
        return self.name

class ClientAccount(Base):
    container_client = models.ForeignKey(Container, on_delete=models.PROTECT, blank=True, null=True)
    client_info = models.ForeignKey(Client, on_delete=models.PROTECT, blank=True, null=True, related_name='client_account')
    debt_usd = models.FloatField(verbose_name="Qarz USD", default=0) 
    debt_uzs = models.FloatField(verbose_name="Qarz UZS", default=0) 
    

class Order(Base): #order
    CURRENCY_TYPE = (
        (1, "USD"),
        (2, "UZS")
    )
    container_order = models.ForeignKey(Container, on_delete=models.PROTECT, blank=True, null=True, related_name='orders')
    customer = models.ForeignKey(Client, on_delete=models.PROTECT, blank=True, null=True)
    currency = models.IntegerField(choices=CURRENCY_TYPE, default=2)
    sale_exchange_rate = models.IntegerField(verbose_name="Valyuta kursi")
    discount = models.FloatField(default=0)
    debt_status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    @property
    def total_summa(self):
        order_sum = 0
        for item in self.items.all():
            if self.currency == 1:
                order_sum += item.total_price
            if self.currency == 2:
                order_sum += item.total_price / self.sale_exchange_rate
            
        return order_sum - self.discount
    
    @property
    def self_total_summa(self):
        order_sum = 0
        for item in self.items.all():
            if self.currency == 1:
                order_sum += item.total_price
            if self.currency == 2:
                order_sum += item.total_price
        
  
            
        return order_sum - self.discount
    

        
    
    
    def __str__(self) -> str:
        return f"{self.customer} | {self.total_summa} | {self.debt_status} "



class OrderItem(Base):
    order_item = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_item = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Mahsulot", related_name='pro_items')
    product_cost = models.FloatField(verbose_name="Mahsulot narxi")
    amount_sold = models.FloatField(verbose_name="Sotilgan miqdori | dona")
    return_qty = models.FloatField(default=0,verbose_name="Qaytarilgan tovar miqdori", blank=True, null=True)
    
    @property
    def total_price(self):
        return self.product_cost * self.amount_sold
    
    def __str__(self) -> str:
        return f"{self.product_item} | {self.product_cost} | {self.amount_sold} "
    
    
class Payment(Base):
    client_account = models.ForeignKey(ClientAccount, on_delete=models.PROTECT, blank=True, null=True)
    CURRENCY_TYPE = (
        (1, "USD"),
        (2, "UZS")
    )
    currency = models.IntegerField(choices=CURRENCY_TYPE, default=2)
    sale_exchange_rate = models.IntegerField(verbose_name="Valyuta kursi", default=0)
    payment_amount = models.FloatField(verbose_name="To'langan summa", default=0)
    
    def __str__(self) -> str:
        return f"{self.client_account} | {self.payment_amount} "
    

class Note(Base):
    text = models.TextField()
    date_of_notice = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.text
