from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
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
    
    
class ContainerProductsDetailView(View):
    
    def get(self, request, pk):
        product_sizes = ProductSize.objects.all()
        
        container = Container.objects.filter(id=pk,status=True)[0]
        container_products = container.container_products.all()
   
        context = {
            "container":container,
            "product_sizes":product_sizes
        }
        
        return render(request, 'container-products-detail.html', context)
    
    
    def post(self, request, pk):
        
        if int(request.POST['select_size']) > 0:
            calc_wood = calc_end_write(request,pk)
        else:
            print("error select tanlash kere")
        
        
        return  redirect(f'/container-products-detail/{pk}')
    
    
class ContainerTradeDetailView(View):
    
    def get(self, request,pk):
        
        container = Container.objects.filter(id=pk,status=True)[0]
        clients = Client.objects.all()
     
        
        context = {
            "container":container,
            "clients":clients
        }
        
        return render(request, 'container-trade-detail.html', context)
    
    
class ContainerExpenceDetailView(View):
    def get(self, request, pk):
        
        container = Container.objects.filter(id=pk,status=True)[0]
        
        print(container.name)
        
        context = {
              "container":container,
        }
        
        return render(request, 'container-expence-detail.html',context)
    
    
    


    
class Clientiew(View):
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

    
class PaymentView(View):
    def get(self, request):
        return render(request, 'payments.html')
    
    
class GeneralExpence(View):
    def get(self, request):
        return render(request, 'general-expenses.html')
    

    
    

    
    
    
class ArchiveContainers(View):
    def get(self,request):
        return render(request, 'archive-containers.html')
    
    
class ArchiveContainerDetail(View):
    def get(self,request):
        return render(request, 'archive-container-detail.html')
    
    
    
    
class AuthLoginView(LoginView):
    template_name = 'auth-login.html' 

    def form_invalid(self, form):
        
        messages.error(self.request, 'Login yoki parol noto`g`ri!')
        
        return super().form_invalid(form)
    

class CustomLogoutView(LogoutView):
    next_page = '/login'