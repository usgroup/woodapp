from django.views import View
from django.http import JsonResponse
from .models import *
from datetime import datetime, date
from .others_func import metr_to_cube, process_order_data, calc_end_write
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .decorator_handle import check_active_user, check_active_user_view




class AddSizeView(View):
    
    @check_active_user
    def post(self, request):
        size_x = float(request.POST.get('product_size_x'))
        size_y = float(request.POST.get('product_size_y'))
        size_z = float(request.POST.get('product_size_z'))
        
        check_product_size = ProductSize.objects.filter( 
            product_size_x=size_x,
            product_size_y=size_y,
            product_size_z=size_z,
            status=True
            )
        
        if check_product_size.exists():
            
            return JsonResponse({'status':400,'message':"Ushbu o'lcham hozirda mavjud !"})
        
        else:
            product_size = ProductSize.objects.create(
                product_size_x=size_x,
                product_size_y=size_y,
                product_size_z=size_z
                )

            data = {
                "size_x": float(product_size.product_size_x),
                "size_y": float(product_size.product_size_y),
                "size_z": float(product_size.product_size_z),
                "id":product_size.id,
            
            }
            
           

            return JsonResponse({'status':200,'message':"Yangi o'lcham qo'shildi !", "data": data})
    

class UpdateSizeView(View):
    @check_active_user
    def post(self, request):
        product_size_id = int(request.POST['product_size_id'])
        update_size_x = float(request.POST['update_size_x'])
        update_size_y = float(request.POST['update_size_y'])
        update_size_z = float(request.POST['update_size_z'])
        
        
        check_product_size = ProductSize.objects.filter( 
            product_size_x=update_size_x,
            product_size_y=update_size_y,
            product_size_z=update_size_z
            )
        
        if check_product_size.exists():
            
            return JsonResponse({'status':400,'message':"Ushbu o'lcham hozirda mavjud !"})
        
        else:
            product_size = ProductSize.objects.filter(id=product_size_id)[0]
            
            product_size.product_size_x = update_size_x
            product_size.product_size_y = update_size_y
            product_size.product_size_z = update_size_z
            product_size.save()
            
            data = {
                "product_size_x": product_size.product_size_x ,
                "product_size_y": product_size.product_size_y,
                "product_size_z":product_size.product_size_z,
                "id":product_size.id
            }
    
            return JsonResponse({'status':200, 'message': "O'lcham yangilandi !","data":data})
    

class DeleteSizeView(View):
    @check_active_user
    def get(self, requets):
        id = int(requets.GET['id'])
        product_size = ProductSize.objects.filter(id=id).first()
        product_size.status = False
        product_size.save()
        data = {
            "id":id
        }
        
        return JsonResponse({'status': 200, 'message': "O'lcham o'chirildi !", "data": data})
    
class UpdateContainerInfoView(View):
    @check_active_user
    def post(self, request):
        id = int(request.POST['container_id'])
        name = request.POST['name']
        date = datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
        
        container = Container.objects.filter(id=id)[0]
        
        container.name = name
        container.come_date = date
        container.save()
        
   
        data = {
            "container_name":container.name,
            "container_come_date": container.come_date.strftime('%d/%m/%Y')
        }
        
        
        
        return JsonResponse({'status': 200, 'message': "Konteyner ma'lumotlari yangilandi !", "data": data})

        
        
class EditProductInfoView(View):
    
    @check_active_user
    def post(self, request):
        product_size_id = int(request.POST['select_size'])
        product_come_cost = float(request.POST['come_cost'])
        product_qty = int(request.POST['product_qty'])
        product_id = int(request.POST['product_id'])
        
        
        product_size = ProductSize.objects.filter(id=product_size_id)[0]  #new size
        
        product = Product.objects.filter(id=product_id)[0]
        
        new_cube = metr_to_cube(product_size.product_size_x , product_size.product_size_y , product_size.product_size_z , product_qty)
        
        difference = product.product_qty - product.rest_qty       
        
        new_rest_qty = product_qty - difference
        
        new_rest_cube = metr_to_cube(product_size.product_size_x , product_size.product_size_y , product_size.product_size_z , new_rest_qty)
        
        product.product_size = product_size
        product.product_qty = product_qty
        product.product_cube = new_cube
        product.come_cost = product_come_cost
        product.rest_cube = new_rest_cube
        product.rest_qty = new_rest_qty
        

        
        product.save()
        
  
        
        data = {
            "product_size":f"{product_size.product_size_x} x {product_size.product_size_y} x {product_size.product_size_z}",
            "product_qty":product.product_qty,
            "product_cube":product.product_cube,
            "rest_cube": product.rest_cube,
            "rest_qty":product.rest_qty,
            "come_cost":product.come_cost,
            "product_size_id":product_size_id,
            "product_id":product_id
        }   
        
            
            
        return JsonResponse({'status': 200, 'message': "Mahsulot ma'lumotlari yangilandi !", "data": data})


       
class DeleteProduct(View):
    @check_active_user
    def post(self, request):
        product_id = int(request.POST['product_id'])
        
        Product.objects.filter(id=product_id)[0].delete()
        
        data = {
            "product_id":product_id
        }
        
        return JsonResponse({'status': 200, 'message': "Mahsulot o'chirildi !", "data": data})

        
        
class EditClientView(View):
    @check_active_user
    def post(self, request):
        name = request.POST['editName']
        phone = request.POST['editPhone']
        client_id = int(request.POST['client_id'])
        
        client = Client.objects.filter(id=client_id)[0]
        
        client.name = name
        client.phone = phone
        client.save()
                
                
      
        data = {
            "client_name":client.name,
            "client_phone":client.phone,
            "client_debt_usd":client.debt_usd,
            "client_debt_uzs":client.debt_uzs,
            "client_id":client.id

        }
        
        
        
        return JsonResponse({'status': 200, 'message': "Mijoz ma'lumotlari yangilandi !", "data": data})

    
class CreateOrderView(View):
    
    @check_active_user
    def post(self, request):
        currencyType = int(request.POST['currencyType'])
        usd_currency = float(request.POST['usd_currency'])
        client_id = int(request.POST['client'])
        totalSumma = float(request.POST['totalSumma'])
        debt_check = request.POST.get('debt_check', None)
        container_id = request.POST['container_id']
        general_summa = float(request.POST['general_summa'])
        
        
        discount = totalSumma - general_summa
        
        container = Container.objects.filter(id=int(container_id)).first()
       
      
        if usd_currency <= 0:
            return JsonResponse(data={'status':400,'error_message': 'Valyuta kursni kiritishni unutdingiz !'})
        
        if general_summa <= 0:
            return JsonResponse(data={'status':400,'error_message': 'Notogri qiymat kiritdingiz !'})

        try:
            # debt_check = request.POST['debt_check']
            
            if debt_check is not None and client_id == 0:
                return JsonResponse(data={'status':400,'error_message': 'Nasiya savdoda mijoz kiritish muhim !'})
           
           
            if debt_check is not None and client_id > 0:
                client = Client.objects.filter(id=client_id)[0]
               
                order = Order.objects.create(
                                container_order=container,
                                customer=client,
                                currency=currencyType,
                                sale_exchange_rate=usd_currency,
                                discount=discount,
                                debt_status=True,
                            )
                
                client_account, created = ClientAccount.objects.get_or_create(
                    container_client=container,
                    client_info=client,
                )
                
                
                
                if currencyType == 1:
                    client_account.debt_usd -= general_summa
                else:
                    client_account.debt_uzs -= general_summa
                    
                client_account.save()
        except:
            pass
            
        if client_id > 0 and debt_check == None:
            client = Client.objects.filter(id=client_id)[0]
            order = Order.objects.create(
                    container_order=container,
                    customer=client,
                    currency=currencyType,
                    sale_exchange_rate=usd_currency,
                    discount=discount,
                    debt_status=False,
                )
            if currencyType == 1:
                container.paid_amount += general_summa
            if currencyType == 2:
                container.paid_amount += (general_summa / order.sale_exchange_rate)
            
            
            
            
            
        if  debt_check == None and client_id == 0:
            order = Order.objects.create(
                    container_order=container,
                    currency=currencyType,
                    sale_exchange_rate=usd_currency,
                    discount=discount,
                    debt_status=False,
                )
            if currencyType == 1:
                container.paid_amount += general_summa
            if currencyType == 2:
                container.paid_amount += (general_summa / order.sale_exchange_rate)
                
          
        order_data = process_order_data(request)
        
        for i in order_data:
            product = Product.objects.filter(id=int(i['product_id']))[0]

            OrderItem.objects.create(
                order_item=order,
                product_item=product,
                product_cost=float(i['product_cost']),
                amount_sold=float(i['amount_sold']),
           
            )
            
            new_qty = product.rest_qty - int(i['amount_sold'])
            product.rest_cube = metr_to_cube(product.product_size.product_size_x,product.product_size.product_size_y, product.product_size.product_size_z, new_qty)
            product.rest_qty = new_qty
            
            product.save()
        
        
        
        counter = 0
        check_products_count = Product.objects.filter(product_container=container)
        
        for p in check_products_count:
            counter += p.rest_qty
            
        
        if counter <= 0:
            container.status = False
            container.end_date=date.today()
            
        container.save()
            
        
        #message add 
        return JsonResponse({'status': 200, 'message': "Mahsulot sotildi ! To'lov qilishni unutmang !"})

    
    
class EditOrderItem(View):
    @check_active_user
    def post(self, request):
        item_id = int(request.POST['order_item_id'])
        qty_item = int(request.POST['qty_item'])
        cost_item = int(request.POST['cost_item'])
        
        order_item = OrderItem.objects.filter(id=item_id).first()
        last_product = order_item.product_item ## product
        last_product_size = order_item.product_item.product_size ## product size
        order = order_item.order_item ## order
        last_amount_sold = order_item.amount_sold
        last_product_cost = order_item.product_cost 
        
        last_product.rest_qty += last_amount_sold
        last_cube = metr_to_cube(last_product_size.product_size_x, last_product_size.product_size_y, last_product_size.product_size_z, last_amount_sold  )
        last_product.rest_cube += float(last_cube)
        
        ##edit
        
        last_product.rest_qty -= qty_item
        new_cube = metr_to_cube(last_product_size.product_size_x, last_product_size.product_size_y,last_product_size.product_size_z, qty_item  )
        
        order_item.product_cost  = cost_item
        last_product.rest_cube -= float(new_cube)
        
        order_item.amount_sold = qty_item
        
        if order.debt_status:
        
            client_account = ClientAccount.objects.filter(container_client=order.container_order, client_info=order.customer).first()
            
            if order.currency == 1:
                client_account.debt_usd -= -(last_product_cost * last_amount_sold)
                client_account.debt_usd += -(cost_item * qty_item)
                
            if order.currency == 2:
                client_account.debt_uzs -= -(last_product_cost * last_amount_sold)
                client_account.debt_uzs += -(cost_item * qty_item)
            
            client_account.save()
            
        order_item.save()
        last_product.save()
        
                    
        
        return JsonResponse({'status': 200, 'message': "Buyurtmaga o'zgarishlar kiritildi !"})

    
    
class ReturnOrderItem(View):
    
    def post(self,request):
        order_item_id = int(request.POST['order_item_id'])
        return_qty = int( request.POST['return_qty'])
        
        order_item = OrderItem.objects.filter(id=order_item_id).first()
        
        last_product = order_item.product_item ## product
        last_product_size = order_item.product_item.product_size ## product size
        order = order_item.order_item ## order
        
        last_amount_sold = order_item.amount_sold
        last_product_cost = order_item.product_cost 
        
        
        last_product.rest_qty += last_amount_sold
        last_cube = metr_to_cube(last_product_size.product_size_x, last_product_size.product_size_y, last_product_size.product_size_z, last_amount_sold  )
        last_product.rest_cube += float(last_cube)
        
        # return
        order_item.return_qty = 0
        order_item.return_qty += return_qty
        new_qty = last_amount_sold - return_qty
        
        
        last_product.rest_qty -= new_qty
        last_cube = metr_to_cube(last_product_size.product_size_x, last_product_size.product_size_y, last_product_size.product_size_z, new_qty  )
        last_product.rest_cube -= float(last_cube)
        
        order_item.amount_sold = new_qty   
        
        if order.debt_status:
        
            client_account = ClientAccount.objects.filter(container_client=order.container_order, client_info=order.customer).first()
            
            if order.currency == 1:
                client_account.debt_usd -= -(last_product_cost * last_amount_sold)
                client_account.debt_usd += -(last_product_cost * new_qty)
                
            if order.currency == 2:
                client_account.debt_uzs -= -(last_product_cost * last_amount_sold)
                client_account.debt_uzs += -(last_product_cost * new_qty)
            
            client_account.save()
        
        order_item.save()
        last_product.save()
        
        return JsonResponse({'status': 200, 'message': "Buyurtma qaytarib olindi !"})

        
        
    

    
class AddExpenseTypeView(View):
    @check_active_user
    def post(self, request):
        
        expense_type_name = request.POST['expense_type_name']
        
        expense_type = ExpenseType.objects.create(title=expense_type_name)
        
        data = {
            "id": expense_type.id,
            "title": expense_type.title,
        }
        
        
        return JsonResponse({'status':200,'message': "Chiqim turi qo'shildi !", "data":data})


class EditExpenseTypeView(View):
    @check_active_user
    def get(self, request):
        
        expense_type_id = request.GET['expense_id']
        expense_type_title = request.GET['expense_type_title']

        
        expense_type = ExpenseType.objects.filter(id=expense_type_id).first()
        expense_type.title = expense_type_title
        expense_type.save()
    
        
        
        data = {
            "id": expense_type.id,
            "title": expense_type.title,
        }
                
        return JsonResponse({'status':200,'message': "Chiqim turi ma'lumotlari yangilandi !", "data":data})

    
    @check_active_user
    def post(self, request):
        

        expense_type_title = request.POST.get('expense_type_title', None)
        expense_type_id = int( request.POST.get('expense_type_id', None))

        
        expense_type = ExpenseType.objects.filter(id=expense_type_id).first()
        expense_type.title = expense_type_title
        expense_type.save()
    
        
        data = {
            "id": expense_type.id,
            "title": expense_type.title,
        }
                
        return JsonResponse({'status':200,'message': "Chiqim turi ma'lumotlari yangilandi !", "data":data})


class DeleteExpenseTypeView(View):
    @check_active_user
    def get(self, requets):
        id = int(requets.GET['id'])
        expense_type = ExpenseType.objects.filter(id=id).first()
        expense_type.is_active = False
        expense_type.save()

        data = {
            "id":id
        }
        
        return JsonResponse({'status': 200, 'message': "Chiqim turi o'chirildi !", "data": data})



class CreateMainExpenseView(View):
    @check_active_user
    def post(self, request):
        expense_type_id = int(request.POST['expense_type'])
        worker_id = request.POST.get('worker', None)
        currency = int(request.POST['currency'])
        ex_sum = float(request.POST['ex_sum'])
        exchange_rate = int(request.POST['exchange_rate'])
        checked_items = request.POST.getlist('checked_items[]')
        switchOnOff = request.POST.getlist('switchOnOff[]')
        
        try:
            expense_type = ExpenseType.objects.get(id=expense_type_id)
        except:
            workers = Worker.objects.get(id=int(worker_id))
        
        # expense_summa = divide(currency, exchange_rate , ex_sum )
        
        if not switchOnOff:
            expense = Expense.objects.create(
                expense_type=expense_type,
                currency=currency,
                expense_summa=ex_sum,
                exchange_rate=exchange_rate,
            )
            expense.containers.set(checked_items)  
            expense.save() 
        else:
            expense = Expense.objects.create(
                    workers=workers,
                    currency=currency,
                    expense_summa=ex_sum,
                    exchange_rate=exchange_rate,
                )
            expense.containers.set(checked_items)  
            expense.save() 
          

        
        return JsonResponse({'status':200,'message': "Chiqim qilindi !"})
    
class EditExpenseView(View):
    
    def get(self, request):
        
        expense_id = int(request.GET['expense_id'])
        expense = Expense.objects.filter(id=expense_id).first()
        expense.is_active = False
        expense.save()
        
        return JsonResponse({'status':200,'message': "Chiqim o'chirildi !"})
        
    
    def post(self, request):
        expense_id = int(request.POST['expense_id'])
        expense_summa = float(request.POST['expense_summa'])
        exchange_rate = int(request.POST['exchange_rate'])
        
        expense = Expense.objects.filter(id=expense_id).first()
        expense.expense_summa = expense_summa
        expense.exchange_rate = exchange_rate
        expense.save()

        
        return JsonResponse({'status':200,'message': "Chiqim tahrirlandi !"})

    
    
class EditWorkerView(View):
    @check_active_user_view
    def post(self,request):
        worker_id = int(request.POST['worker_id'])
        name = request.POST['name']
        phone = request.POST['phone']
        birth_date = request.POST['birth_date']
        
        
        worker = Worker.objects.filter(id=worker_id).first()
        worker.name = name
        worker.phone = phone
        worker.birth_date = birth_date
        worker.save()
        return redirect('/workers')

class DeleteWorkerView(View):
    
    @check_active_user
    def get(self,request):
        id = request.GET.get('id')
        worker = Worker.objects.filter(id=int(id)).first()
        worker.delete()
        
        return JsonResponse({'status':200,'message': "Ishchi o'chirildi !"})



class SearchContainerView(View):
    
    def get(self, request):
        
        value =  request.GET.get('value')
        archive =  request.GET.get('archive')

        
        result = {
            'status':200,
            'data':[]
        }

        value = value.strip() if value else None
        
        query = Q(name__icontains=value) | Q(come_date__icontains=value)
        
        
        if value:
            if archive == 'true':
                containers = Container.objects.filter(query, status=False)
            if archive == 'false':
                containers = Container.objects.filter(query, status=True)
                
            
            for c in containers:
                date_obj = datetime.strptime(str(c.come_date), '%Y-%m-%d')
                formatted_date_str = date_obj.strftime('%d/%m/%Y')
                
                result['data'].append(
                    {
                    "container_id":c.id,
                    "container_name":c.name,
                    "container_come_date":formatted_date_str,
                    }
                )
        else:
            if archive == 'true':
                containers = Container.objects.filter(status=False)

            if archive == 'false':
                containers = Container.objects.filter(status=True)
                
            for c in containers:
                date_obj = datetime.strptime(str(c.come_date), '%Y-%m-%d')
                formatted_date_str = date_obj.strftime('%d/%m/%Y')
                result['data'].append(
                    {
                    "container_id":c.id,
                    "container_name":c.name,
                    "container_come_date":formatted_date_str,
                    }
                )
        return JsonResponse(result)
    


class CreatePaymentView(View):
    @check_active_user
    def post(self,request):
        
    
        client_id = int(request.POST['client'])
        container = int(request.POST['container'])
        currency_type = int(request.POST['currency_type'])
        exchange_rate = int(request.POST['exchange_rate'])
        payment_sum = float(request.POST['payment_sum'])
        
        container = Container.objects.filter(id=container).first()
      
        
        client = Client.objects.filter(id=client_id).first()
        client_account = ClientAccount.objects.filter(client_info=client, container_client=container).first()
        
        payment, created = Payment.objects.get_or_create(
            client_account=client_account,
            currency=currency_type,
        )
        if not created:
            payment.sale_exchange_rate = exchange_rate
            payment.payment_amount += payment_sum
        else:
            payment.sale_exchange_rate = exchange_rate
            payment.payment_amount = payment_sum
        
        if currency_type == 1:
            client_account.debt_usd += payment_sum
            container.paid_amount += payment_sum
        else:
            client_account.debt_uzs += payment_sum 
            container.paid_amount += (payment_sum / exchange_rate)
            
            
        
        
        payment.save()
        client_account.save()
        container.save()

        return JsonResponse({'status':200,'message': "To'lov amalga oshirildi !"})

    
class EditPaymentView(View):
    @check_active_user
    def post(self, request):
        payment_id = int(request.POST['payment_id'])
        payment_sum = float(request.POST['payment_sum'])
        currency_type = int(request.POST['currency_type'])
        exchange_rate = int(request.POST['exchange_rate'])
        
        
        payment = Payment.objects.filter(id=payment_id).first()
        container = payment.client_account.container_client
        last_client_info = payment.client_account
        payment.payment_amount = payment.payment_amount
        last_currency = payment.currency
        last_sale_exchange_rate = payment.sale_exchange_rate
        
        if last_currency == 2:
            container.paid_amount -= (payment.payment_amount/last_sale_exchange_rate)
            last_client_info.debt_uzs -= payment.payment_amount
            payment.payment_amount -= payment.payment_amount
        if last_currency == 1:
            container.paid_amount -= payment.payment_amount
            last_client_info.debt_usd -= payment.payment_amount
            payment.payment_amount -= payment.payment_amount
            
        
        ###
        
        if currency_type == 2:
            container.paid_amount += (payment_sum / exchange_rate)
            last_client_info.debt_uzs += payment_sum
            
            payment.payment_amount += payment_sum

        if currency_type == 1:
            container.paid_amount += payment_sum 
            last_client_info.debt_usd += payment_sum
            
            payment.payment_amount += payment_sum

            
            
        last_client_info.save()
        # payment.payment_amount.save()
        container.save()
        payment.save()

        return JsonResponse({'status':200,'message': "To'lov ma'lumotlari yangilandi !"})

        
    

class GetClientDebt(View):
    @check_active_user
    def post(self, request):
        client_id = int(request.POST['client_id'])
        container_id = int(request.POST['container_id'])
        client = Client.objects.filter(id=client_id).first()
        container = Container.objects.filter(id=container_id).first() 
        
        if not client or not container:
            return JsonResponse({'status': 400, 'message': 'Invalid client or container ID'}, status=400)
        
        client_account, created = ClientAccount.objects.get_or_create(client_info=client, container_client=container)
        
        data = {
            "debt_usd": client_account.debt_usd,
            "debt_uzs": client_account.debt_uzs,
        }
        
        return JsonResponse({'status': 200, 'message': 'Get client debt successfully', 'data': data})
    
    
class FilterOrdersView(View):
    def get(self, request):
        start_date = request.GET['startDate']
        end_date = request.GET['endDate']
        
        container_id = request.GET['container_id']
        container = Container.objects.filter(id=int(container_id)).first()
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date =  datetime.strptime(end_date, '%Y-%m-%d').date()
            
            orders = Order.objects.filter(container_order=container, created_at__range=[start_date, end_date])
            
        except :
            orders = Order.objects.filter(container_order=container)


        data = []
        for order in orders:
            order_data = {
                'id': order.id,
                'customer_name': order.customer.name,
                'total_summa': order.total_summa,
                'currency': order.currency,
                'discount': order.discount,
                'created_at': order.created_at.strftime('%Y-%m-%d'),
                'items': []
            }
            for item in order.items.all():
                order_data['items'].append({
                    'id': item.id,
                    'product_size': f"{item.product_item.product_size.product_size_x} x {item.product_item.product_size.product_size_y} x {item.product_item.product_size.product_size_z}",
                    'amount_sold': item.amount_sold,
                    'product_cost': item.product_cost,
                    'total_price': item.total_price
                })
            data.append(order_data)
            
            
        return JsonResponse({'status': 200, 'message': 'filter order successfully', 'data': data})
    

class FilterExpenseView(View):
    def get(self, request):
        start_date = request.GET['startDate']
        end_date = request.GET['endDate']
        
        data = []
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date =  datetime.strptime(end_date, '%Y-%m-%d').date()
            
            expenses = Expense.objects.filter(is_active=True,created_at__range=[start_date, end_date])
            
        except :
            expenses = Expense.objects.filter(is_active=True)
        
        for e in expenses:
            expense_data = {
                "expense_id":e.id,
                "created_at":e.created_at.strftime('%Y-%m-%d'),
                "expense_type":e.expense_type.title,
                "workers":e.workers,
                "currency":e.currency,
                "expense_summa":e.expense_summa,
                "container_sum":e.container_sum,
                "exchange_rate":e.exchange_rate,
                "containers":[],
                
            }
            for c in e.containers.all():
                expense_data['containers'].append({
                    'name':c.name
                })
            data.append(expense_data)
    
        
        return JsonResponse({'status': 200, 'message': 'filter expense successfully', 'data': data})
        
        


class CutProductView(View):
    @check_active_user
    def post(self, request):
        product_id = int(request.POST['product_id'])
        cut_qty = int(request.POST['cut_qty'])
        
     
        product_ = Product.objects.filter(id=product_id).first()
        
        product_.rest_qty -= cut_qty
        
        new_cube = metr_to_cube(product_.product_size.product_size_x, product_.product_size.product_size_y, product_.product_size.product_size_z, cut_qty)
        
        product_.rest_cube -= new_cube
        
        product, created = Product.objects.get_or_create(
            product_container=product_.product_container,
            product_size=product_.product_size,
            is_cut=True,
        
        )
        product.product_qty += 0
        product.product_cube += 0
        
        product.rest_qty += cut_qty
        product.rest_cube += new_cube
        
        product_.save()
        product.save()
        
        
        
        data = { 
            
        }
        
        return JsonResponse({'status': 200, 'message': 'Mahsulot kesildi !', 'data': data})
    


    
class CreateNoteView(View):
    @check_active_user
    def post(self, request):
        date = request.POST['date']
        text = request.POST['text']
        
        date_of_notice = datetime.strptime(date, '%Y-%m-%d').date()
        
        
        note = Note.objects.create(
            text = text,
            date_of_notice = date_of_notice
        )
        
        
        return JsonResponse({'status': 200, 'message': 'Eslatma yaratildi!'})


class EditNoteView(View):
    @check_active_user
    def post(self, request):
        date = request.POST['date']
        text = request.POST['text']
        note_id = int(request.POST['note_id'])
        
        note = Note.objects.filter(id=note_id).first()
        note.text = text
        note.date_of_notice = date
        note.save()
        
        
        print()
        print(request.POST)
        print()
        
        return redirect('/notes')


class DeleteNoteView(View):
    @check_active_user
    def get(self, request):
        
        id  = int(request.GET['id'])
        
        note = Note.objects.filter(id=id).first()
        note.delete()
        
        return JsonResponse({'status': 200, 'message': "Eslatma o'chirildi !"})

    

class EditNoteStatusView(View):
    @check_active_user
    def get(self, request):
        id  = int(request.GET['id'])
        status = request.GET['status']
        
            
        note = Note.objects.filter(id=id).first()
        
        if status == 'active':
            note.is_active = True
        if status == 'disactive':
            note.is_active = False
        
        note.save()

            
        return JsonResponse({'status': 200, 'message': "Eslatma o'qildi !"})




@method_decorator(csrf_exempt, name='dispatch')
class AddUserView(View):
    @check_active_user
    def post(self, request):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')

        if not all([username, first_name, user_type, password]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required'})

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})

        user = CustomUser(
            username=username,
            first_name=first_name,
            is_staff=(user_type == '1')
        )
        user.set_password(password)
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User added successfully'})

# Edit an existing user

@method_decorator(csrf_exempt, name='dispatch')
class EditUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')

        if not all([username, first_name, user_type]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required'})

        user.username = username
        user.first_name = first_name
        
        print(user_type)
        print(user_type)
        
        if user_type == '1':
            user.is_staff = True
            
        if user_type == '2':
            user.is_staff = False
            
        if password:
            user.set_password(password)
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User updated successfully'})

# Delete a user

@method_decorator(csrf_exempt, name='dispatch')
class DeleteUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'User deleted successfully'})

        




