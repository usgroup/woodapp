from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime
from .others_func import calc_end_write


class HomeView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        containers = Container.objects.filter(status=True).order_by('-id')
        all_product_size = ProductSize.objects.all()
        
        context = {
            "containers":containers,
            "all_product_size":all_product_size
        }
        
        return render(request, 'index.html',context)

    def post(self, request):
        
        container_name = request.POST['container_name']
        come_date = datetime.strptime(request.POST['come_date'], "%Y-%m-%d").date()
        
        container = Container.objects.create(name=container_name, come_date=come_date)
        
        pk = container.id
     
        
        return redirect(f'/container-products-detail/{pk}')
    
    
class ContainerProductsDetailView(LoginRequiredMixin,View):
    
    def get(self, request, pk):
        product_sizes = ProductSize.objects.all()
        
        general_expenses = 0
        
        container = Container.objects.filter(id=pk,status=True)[0]
        container_products = container.container_products.all()
        
        expenses = Expense.objects.filter(containers__id=pk)
        
        # #statictic
        for e in expenses:  #buni qoshish kerak generalga 
            general_expenses += e.container_sum
       
        for c in container_products: # productlarni qo'shilmasi
            general_expenses += c.total_product_sum
     
        profit = container.total_paid_sum_usd - general_expenses
   
        context = {
            "container":container,
            "product_sizes":product_sizes,
            "general_expenses":general_expenses,
            "total_sales_revenue_usd":container.total_sales_revenue_usd,
            "total_paid_sum_usd":container.total_paid_sum_usd,
            "profit": profit
            
        }
        
      
        
        
        return render(request, 'container-products-detail.html', context)
    
    
    def post(self, request, pk):
        
        if int(request.POST['select_size']) > 0:
            calc_wood = calc_end_write(request,pk)
        else:
            print("error select tanlash kere")
        
        
        return  redirect(f'/container-products-detail/{pk}')
    
    
class ContainerTradeDetailView(LoginRequiredMixin,View):
    
    def get(self, request,pk):
        
        container = Container.objects.filter(id=pk,status=True)[0]
        clients = Client.objects.all()
     
        
        context = {
            "container":container,
            "clients":clients
        }
        
        return render(request, 'container-trade-detail.html', context)
    
    
class ContainerExpenceDetailView(LoginRequiredMixin,View):
    def get(self, request, pk):
        
        container = Container.objects.filter(id=pk,status=True)[0]
        
        print()
        print(container.expense_set.all())
        print()
   
        context = {
            "container":container,
        }
        
        return render(request, 'container-expence-detail.html',context)
    
    
    


    
class Clientiew(LoginRequiredMixin,View):
    def get(self, request):
        clients = Client.objects.all().order_by('-id')
        context = {
            "clients":clients
        }
        return render(request, 'clients.html',context)
    
    def post(self,request):
        name = request.POST['name']
        phone = request.POST['phone']
        
        Client.objects.create(name=name,phone=phone)
        
        
        return redirect('/clients')

    
class PaymentView(LoginRequiredMixin,View):
    def get(self, request):
        clients = Client.objects.all()
        context = {
            "clients":clients
        }
        return render(request, 'payments.html', context )
    
    def post(self, request):
        print()
        print(request.POST)
        print()
        
        
        return redirect('/payments')
    
    
class GeneralExpence(LoginRequiredMixin,View):
    def get(self, request):
        
        expense_types = ExpenseType.objects.all()
        workers = Worker.objects.all()
        containers = Container.objects.filter(status=True)
        
        context = {
            "expense_types":expense_types,
            "workers":workers,
            "containers":containers
        }
        
        return render(request, 'general-expenses.html', context)
    
class WorkerView(LoginRequiredMixin,View):
    def get(self, request):
        
        workers = Worker.objects.all()
        
        context = {
            "workers":workers
        }
        
        return render(request, 'workers.html', context)
    
    def post(self,request):
        name = request.POST['name']
        phone = request.POST['phone']
        birth_date = request.POST['birth_date']
        
        
        worker = Worker.objects.create(
            name=name,
            phone=phone,
            birth_date=birth_date
            )
        
        return redirect('/workers')
        
    

    
    
    
class ArchiveContainers(LoginRequiredMixin,View):
    def get(self,request):
        
        containers = Container.objects.filter(status=True).order_by('-id')
        
        context = {
            "containers":containers
        }
        return render(request, 'archive-containers.html', context)
    
    
class ArchiveContainerDetail(LoginRequiredMixin,View):
    def get(self,request, pk):
        
        container = Container.objects.filter(id=int(pk)).first()
        order_items = OrderItem.objects.filter(product_item__product_container__id=int(pk))
        
        unique_orders = set()
        
        
        for item in order_items:
            unique_orders.add(item.order_item)
        
        
        
        context = {
            "container":container,
            "unique_orders":unique_orders
        }
        
        return render(request, 'archive-container-detail.html', context)
    
    


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to a home page or dashboard
        else:
            messages.error(request, "Login yoki parol notog'ri")
            return render(request, 'auth-login.html', {'error': 'Invalid credentials'})
    return render(request, 'auth-login.html')

def logout_view(request):
    logout(request)
    return redirect('/login')


def handler_404(request, exception):
    return render(request, 'error-404.html')

def handler_500(request):
    return render(request, 'errors/500.html')
