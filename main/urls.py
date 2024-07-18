from django.urls import path
from .views import *
from .ajax import *

app_name = 'main'


urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('container-products-detail/<int:pk>',ContainerProductsDetailView.as_view(), name='container-products-detail'),
    path('container-trade-detail/<int:pk>',ContainerTradeDetailView.as_view(), name='container-trade-detail'),
    path('container-expence-detail/<int:pk>',ContainerExpenceDetailView.as_view(), name='container-expence-detail'),
    path('general-expense',GeneralExpence.as_view(), name='general-expense'),
    path('clients',Clientiew.as_view(), name='clients'),
    path('payments',PaymentView.as_view(), name='payments'),
    
    
    path('login',AuthLoginView.as_view(), name='login'),
    path('logout',  CustomLogoutView.as_view(), name='logout'),
    
    
    path('archive-containers',ArchiveContainers.as_view(), name='archive_containers'),
    path('archive-container-detail',ArchiveContainerDetail.as_view(), name='archive_container_detail'),
    
    
    #ajax
    path('add-size/', AddSizeView.as_view(), name='add-size'),
    path('update-size/', UpdateSizeView.as_view(), name='update-size'),
    path('update-container-info/', UpdateContainerInfoView.as_view(), name='update-container-info'),
    path('edit-product-info/', EditProductInfoView.as_view(), name='edit-product-info'),
    path('delete-product/', DeleteProduct.as_view(), name='delete-product'),
    path('edit-client', EditClientView.as_view(), name='edit-client'),
    path('create-order', CreateOrderView.as_view(), name='create-order'),
    path('add-expense-type', AddExpenseTypeView.as_view(), name='add-expense-type'),
    path('edit-expense-type', EditExpenseTypeView.as_view(), name='edit-expense-type'),
    
]