from django.urls import path
from .views import *
from .ajax import *

app_name = 'main'


urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('container-products-detail/<int:pk>',ContainerProductsDetailView.as_view(), name='container-products-detail'),
    path('container-trade-detail/<int:pk>',ContainerTradeDetailView.as_view(), name='container-trade-detail'),
    path('container-expence-detail/<int:pk>',ContainerExpenceDetailView.as_view(), name='container-expence-detail'),
    path('container-trade-history/<int:pk>',ContainerTradeHistoryView.as_view(), name='container-trade-history'),
    path('delete-container',ContainerDeleteView.as_view(), name='delete-container'),
    path('general-expense',GeneralExpence.as_view(), name='general-expense'),
    path('all-expenses',AllExpense.as_view(), name='all-expenses'),
    path('clients',Clientiew.as_view(), name='clients'),
    path('payments',PaymentView.as_view(), name='payments'),
    path('workers',WorkerView.as_view(), name='workers'),
    path('edit-worker', EditWorkerView.as_view(), name='edit-worker'),
    path('notes', NoteView.as_view(), name='notes'),
    path('trash', TrashView.as_view(), name='trash'),
    
    
    path('login',login_view, name='login'),
    path('logout',  logout_view, name='logout'),
    
    path('users',  UsersView.as_view(), name='users'),
    # path('create-user',  CreateUsersView.as_view(), name='create-user'),
    # path('edit-user',  EditUsersView.as_view(), name='edit-user'),
    
    # path('users', UserListView.as_view(), name='user-list'),
    path('add-user/', AddUserView.as_view(), name='add-user'),
    path('edit-user/<int:user_id>/', EditUserView.as_view(), name='edit-user'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete-user'),
    
    
    path('trade-history',ArchiveContainers.as_view(), name='archive_containers'),
    path('archive-product-history-detail/<int:pk>',ArchiveContainerDetail.as_view(), name='archive-product-detail'),
    path('archive-expense-history-detail/<int:pk>',ArchiveContainerExpenseDetail.as_view(), name='archive-expense-container-detail'),
    path('archive-trade-history-detail/<int:pk>',ArchiveContainerTradeDetail.as_view(), name='archive-trade-history-detail'),
    path('back-main-container',BackMainContainer.as_view(), name='back-main-container'),
    path('back-archive-container',BackArchiveContainer.as_view(), name='back-archive-container'),
    
    
    #ajax
    path('add-size/', AddSizeView.as_view(), name='add-size'),
    path('update-size/', UpdateSizeView.as_view(), name='update-size'),
    path('delete-size/', DeleteSizeView.as_view(), name='delete-size'),
    path('update-container-info/', UpdateContainerInfoView.as_view(), name='update-container-info'),
    path('edit-product-info/', EditProductInfoView.as_view(), name='edit-product-info'),
    path('delete-product/', DeleteProduct.as_view(), name='delete-product'),
    
    path('back-product', BackProductView.as_view(), name='back-product'),
    
    path('edit-client', EditClientView.as_view(), name='edit-client'),
    
    path('create-order', CreateOrderView.as_view(), name='create-order'),
    
    path('add-expense-type', AddExpenseTypeView.as_view(), name='add-expense-type'),
    path('edit-expense-type', EditExpenseTypeView.as_view(), name='edit-expense-type'),
    path('delete-expense-type', DeleteExpenseTypeView.as_view(), name='delete-expense-type'),
    
    path('create-main-expense', CreateMainExpenseView.as_view(), name='create-main-expense'),
    path('back-expense', BackExpenseView.as_view(), name='back-expense'),
    path('delete-worker', DeleteWorkerView.as_view(), name='delete-worker'),
    #search
    path('search-container', SearchContainerView.as_view(), name='search-container'),
    path('create-payment', CreatePaymentView.as_view(), name='create-payment'),
    path('edit-payment', EditPaymentView.as_view(), name='edit-payment'),
    path('get-client-debt', GetClientDebt.as_view(), name='get-client-debt'),
    path('edit-order-item', EditOrderItem.as_view(), name='edit-order-item'),
    path('return-order-item', ReturnOrderItem.as_view(), name='return-order-item'),
    
    
    path('delete-order', DeleteOrderView.as_view(), name='delete-order'),
    path('back-order', BackOrderView.as_view(), name='back-order'),
    
    #filter
    path('filter-orders', FilterOrdersView.as_view(), name='filter-orders'),
    path('filter-expenses', FilterExpenseView.as_view(), name='filter-expenses'),
    
    path('cut-product', CutProductView.as_view(), name='cut-product'),
    path('add-cut-product', AddCutProductView.as_view(), name='add_cut_product'),
    path('edit-cut-product', EditCutProductView.as_view(), name='edit_cut_product'),
    
    path('edit-expense',EditExpenseView.as_view(), name='edit-expense'),
    path('create-note',CreateNoteView.as_view(), name='create-note'),
    path('delete-note',DeleteNoteView.as_view(), name='delete-note'),
    path('edit-note',EditNoteView.as_view(), name='edit-note'),
    path('edit-note-status',EditNoteStatusView.as_view(), name='edit-note-status'),
    
]