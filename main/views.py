from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime, date , timedelta
from .others_func import calc_end_write,container_info
from django.utils import timezone

from .decorator_handle import check_active_user_view


class HomeView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        containers = Container.objects.filter(status=True,  is_active=True).order_by('-id')
        all_product_size = ProductSize.objects.filter(status=True)
        
        context = {
            "containers":containers,
            "all_product_size":all_product_size
        }
        
        return render(request, 'index.html',context)

    @check_active_user_view
    def post(self, request):
        
        container_name = request.POST['container_name']
        come_date = datetime.strptime(request.POST['come_date'], "%Y-%m-%d").date()
        
        container = Container.objects.create(name=container_name, come_date=come_date)
        
        pk = container.id
     
        
        return redirect(f'/container-products-detail/{pk}')
    

    
    
class ContainerProductsDetailView(LoginRequiredMixin,View):
    
    def get(self, request, pk):
       
        context = container_info(request, pk)
        context['products'] = Product.objects.filter(product_container=context['container'], is_active=True)
        
      
        
        return render(request, 'container-products-detail.html', context)
    
    @check_active_user_view
    def post(self, request, pk):
        
        if int(request.POST['select_size']) > 0:
            calc_wood = calc_end_write(request,pk)
        else:
            print("error select tanlash kere")
        
        
        return  redirect(f'/container-products-detail/{pk}')
    
    
class ContainerTradeDetailView(LoginRequiredMixin,View):
    
    def get(self, request,pk):
        product_list = []
        context = container_info(request, pk)
        products = Product.objects.filter(product_container=context['container'], is_active=True)
        
        for p in products:
            if p.rest_qty > 0:
                product_list.append(p)
  
        clients = Client.objects.all()
     
        
        context["clients"] = clients
        context["product_list"] = product_list
        
        return render(request, 'container-trade-detail.html', context)
    
    
class ContainerExpenceDetailView(LoginRequiredMixin,View):
    def get(self, request, pk):
        
        context = container_info(request, pk)
        
        return render(request, 'container-expence-detail.html',context)
    


class ContainerTradeHistoryView(View):
    def get(self, request,pk):
       
        
        context = container_info(request, pk)
        
        container = Container.objects.filter(id=int(pk)).first()
        orders = Order.objects.filter(container_order=container, is_active=True).order_by('-id')
        
        context["orders"] = orders
        
        return render(request, 'container-trade-history.html',context)
    

class ContainerDeleteView(View):
    def post(self, request):
        
        container_id = int(request.POST['container_id'])
        container = Container.objects.filter(id=container_id).first()
        container.is_active = False
        container.save()
        
        
        return redirect('/')


    
class Clientiew(LoginRequiredMixin,View):
    def get(self, request):
        clients = Client.objects.all().order_by('-id')
        context = {
            "clients":clients
        }
        return render(request, 'clients.html',context)
    
    @check_active_user_view
    def post(self,request):
        name = request.POST['name']
        phone = request.POST['phone']
        
        Client.objects.create(name=name,phone=phone)
        
        
        return redirect('/clients')

    
class PaymentView(LoginRequiredMixin,View):
    def get(self, request):
        clients = Client.objects.all()
        containers = Container.objects.filter(status=True,  is_active=True)
        payments = Payment.objects.all().order_by('-id')
        
        
        context = {
            "clients":clients,
            "containers":containers,
            "payments":payments,
        }
        return render(request, 'payments.html', context )
    
    
class GeneralExpence(LoginRequiredMixin,View):
    def get(self, request):
        
        expense_types = ExpenseType.objects.filter(is_active=True)
        workers = Worker.objects.all()
        containers = Container.objects.filter(status=True,  is_active=True)
        
        context = {
            "expense_types":expense_types,
            "workers":workers,
            "containers":containers
        }
        
        return render(request, 'general-expenses.html', context)
    
    
class AllExpense(LoginRequiredMixin,View):
    def get(self, request):
        
        expenses = Expense.objects.filter(is_active=True, created_at__date__gte=date.today().replace(day=1))
        
        context = {
            "expenses":expenses,
        }
        
        return render(request, 'all_expenses.html', context)
    
    
class WorkerView(LoginRequiredMixin,View):
    def get(self, request):
        
        workers = Worker.objects.all()
        
        context = {
            "workers":workers
        }
        
        return render(request, 'workers.html', context)
    
    @check_active_user_view
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
        
        containers = Container.objects.filter(status=False,  is_active=True).order_by('-id')
        
        context = {
            "containers":containers
        }
        return render(request, 'archive-containers.html', context)
    
    
class ArchiveContainerDetail(LoginRequiredMixin,View):
    def get(self,request, pk):
        
        context = container_info(request,pk)
        
        orders = Order.objects.filter(container_order=context['container'], is_active=True).order_by('-id')
        
        
        context['unique_orders'] = orders
        
        return render(request, 'archive-container-products-detail.html', context)
    
    
class ArchiveContainerExpenseDetail(LoginRequiredMixin,View):
    def get(self, request, pk):
        
        context = container_info(request,pk)
        
        
       
        return render(request, 'archive-expence-history-detail.html',context)
    
    
class ArchiveContainerTradeDetail(LoginRequiredMixin,View):
      def get(self, request,pk):
        
        context = container_info(request,pk)    

        orders = Order.objects.filter(container_order=context['container'], is_active=True).order_by('-id')
        
        context['orders'] = orders
        
        return render(request, 'archive-trade-history.html',context)
    
    
class BackMainContainer(View):
    def post(self,request):
        container_id = int(request.POST['container_id'])
        
        container = Container.objects.filter(id=container_id).first()
        container.status = True
        container.save()
        
        return redirect('/')
    
    
class BackArchiveContainer(View):
    
    def post(self,request):
        container_id = int(request.POST['container_id'])
        
        container = Container.objects.filter(id=container_id).first()
        container.status = False
        container.save()
        
        return redirect('/trade-history')
        
        
    
    
class NoteView(LoginRequiredMixin,View):
    def get(self, request):
        
        notes = Note.objects.all().order_by('-is_active')
        context = {
            'notes':notes
        }
        return render(request, 'notes.html',context)
    
    
    

class TrashView(View):
    def get(self, request):
        
        thirty_days_ago = timezone.now() - timedelta(days=30)

        old_products = Product.objects.filter(is_active=False, updated_at__lte=thirty_days_ago)
        old_orders = Order.objects.filter(is_active=False, updated_at__lte=thirty_days_ago)
        old_expenses = Expense.objects.filter(is_active=False, updated_at__lte=thirty_days_ago)

        old_products.delete()
        old_orders.delete()
        old_expenses.delete()
        
        products = Product.objects.filter(is_active=False)
        orders = Order.objects.filter(is_active=False)
        expenses = Expense.objects.filter(is_active=False)
        
        context = {
            "products":products,
            "orders":orders,
            "expenses":expenses,
        }
        
        return render(request, 'trash.html', context)
    

class UsersView(LoginRequiredMixin,View):
    def get(self, request):
        
        users = CustomUser.objects.all()
        
        context = {
            "users":users
        }
        
        return render(request, 'users.html', context)
    
    



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
    return render(request, 'error-500.html')
