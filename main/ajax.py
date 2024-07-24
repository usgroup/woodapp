from django.views import View
from django.http import JsonResponse
from .models import *
from datetime import datetime
from .others_func import metr_to_cube, process_order_data, divide, calc_end_write
from django.shortcuts import redirect
from django.db.models import Q



class AddSizeView(View):
    def post(self, request):
        size_x = int(request.POST.get('product_size_x'))
        size_y = int(request.POST.get('product_size_y'))
        size_z = int(request.POST.get('product_size_z'))

        product_size = ProductSize.objects.create(
            product_size_x=size_x,
            product_size_y=size_y,
            product_size_z=size_z
            )


        data = {
            "size_x": float(product_size.product_size_x),
            "size_y": float(product_size.product_size_y),
            "size_z": float(product_size.product_size_y),
            "id":product_size.id,
         
        }

        return JsonResponse({'message': 'Size added successfully',"data": data})
    

class UpdateSizeView(View):
    def post(self, request):
        product_size_id = int(request.POST['product_size_id'])
        update_size_x = float(request.POST['update_size_x'])
        update_size_y = float(request.POST['update_size_y'])
        update_size_z = float(request.POST['update_size_z'])
        
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
  
        return JsonResponse({'message': 'Size updated successfully',"data":data})
    

class DeleteSizeView(View):
    def get(self, requets):
        id = int(requets.GET['id'])
        product_size = ProductSize.objects.filter(id=id).first()
        product_size.delete()

        data = {
            "id":id
        }
        
        return JsonResponse({'status': 200, 'message': 'Product Size deleted successfully', "data": data})
    
class UpdateContainerInfoView(View):
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
        
        
        
        return JsonResponse({'message': 'Container Info updated successfully',"data":data})
        
        
class EditProductInfoView(View):
    
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
        
            
            
        return JsonResponse({'message': 'Product Info updated successfully',"data":data})


       
class DeleteProduct(View):
    def post(self, request):
        product_id = int(request.POST['product_id'])
        
        Product.objects.filter(id=product_id)[0].delete()
        
        data = {
            "product_id":product_id
        }
        
        return JsonResponse({'message': 'Product deleted successfully',"data":data})
        
        
class EditClientView(View):
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
        print()
        print(data)
        print()
        
        
        
        return JsonResponse({'message': 'Produсt deleted successfully',"data":data})
    
class CreateOrderView(View):
    
    def post(self, request):
        currencyType = int(request.POST['currencyType'])
        usd_currency = int(request.POST['usd_currency'])
        client_id = int(request.POST['client'])
        totalSumma = int(request.POST['totalSumma'])
        debt_check = request.POST.get('debt_check', None)
        container_id = request.POST['container_id']
        
        container = Container.objects.filter(id=int(container_id)).first()
        
        print()
        print(container_id)
        print()
        
      
        if usd_currency <= 0:
            return JsonResponse(data={'status':400,'error_message': 'Valyuta kursni kiritishni unutdingiz !'})

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
                                debt_status=True,
                            )
                
                client_account, created = ClientAccount.objects.get_or_create(
                    container_client=container,
                    client_info=client,
                )
                
                print(client_account)
                
                if currencyType == 1:
                    client_account.debt_usd -= totalSumma
                else:
                    client_account.debt_uzs -= totalSumma
                    
                client_account.save()
        except:
            pass
            
        if client_id > 0:
            client = Client.objects.filter(id=client_id)[0]
            order = Order.objects.create(
                    container_order=container,
                    customer=client,
                    currency=currencyType,
                    sale_exchange_rate=usd_currency,
                    debt_status=False,
                )
            
            
            
        else:
            order = Order.objects.create(
                    container_order=container,
                    currency=currencyType,
                    sale_exchange_rate=usd_currency,
                    debt_status=False,
                )
                
        order_data = process_order_data(request)
        
        for i in order_data:
            product = Product.objects.filter(id=int(i['product_id']))[0]

            OrderItem.objects.create(
                order_item=order,
                product_item=product,
                product_cost=int(i['product_cost']),
                amount_sold=int(i['amount_sold']),
           
            )
            
            new_qty = product.rest_qty - int(i['amount_sold'])
            product.rest_cube = metr_to_cube(product.product_size.product_size_x,product.product_size.product_size_y, product.product_size.product_size_z, new_qty)
            product.rest_qty = new_qty
            
            product.save()
        
       
        
        #message add 
        return JsonResponse({'status':200,'message': 'Product sale successfully'})
    
    
class EditOrderItem(View):
    def post(self, request):
        item_id = int(request.POST['order_item_id'])
        qty_item = int(request.POST['qty_item'])
        cost_item = int(request.POST['cost_item'])
        
        print()
        print(request.POST)
        print()
        
        order_item = OrderItem.objects.filter(id=item_id).first()
        last_product = order_item.product_item ## product
        last_product_size = order_item.product_item.product_size ## product size
        last_amount_sold = order_item.amount_sold
        last_product_cost = order_item.product_cost 
        
        last_product.rest_qty += last_amount_sold
        last_cube = metr_to_cube(last_product_size.product_size_x, last_product_size.product_size_y, last_product_size.product_size_z, last_amount_sold  )
        last_product.rest_cube -= float(last_cube)
        
        ##edit
        
        last_product.rest_qty -= qty_item
        new_cube = metr_to_cube(last_product_size.product_size_x, last_product_size.product_size_y,last_product_size.product_size_z, qty_item  )
        
        order_item.product_cost  = cost_item
        last_product.rest_cube += float(new_cube)
        
        order_item.amount_sold = qty_item
        
        order_item.save()
        last_product.save()
        
                        
        
        
        return JsonResponse({'status':200,'message': 'Order item edited successfully'})
        
    

    
class AddExpenseTypeView(View):
    def post(self, request):
        
        expense_type_name = request.POST['expense_type_name']
        
        expense_type = ExpenseType.objects.create(title=expense_type_name)
        
        data = {
            "id": expense_type.id,
            "title": expense_type.title,
        }
        
        print(request.POST)
        
        return JsonResponse({'status':200,'message': 'ExpenseType added successfully', "data":data})


class EditExpenseTypeView(View):
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
                
        return JsonResponse({'status': 200, 'message': 'ExpenseType edited successfully', "data": data})
    
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
                
        return JsonResponse({'status': 200, 'message': 'ExpenseType edited successfully', "data": data})

class DeleteExpenseTypeView(View):
    def get(self, requets):
        id = int(requets.GET['id'])
        expense_type = ExpenseType.objects.filter(id=id).first()
        expense_type.delete()

        data = {
            "id":id
        }
        
        return JsonResponse({'status': 200, 'message': 'ExpenseType deleted successfully', "data": data})



class CreateMainExpenseView(View):
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
        
        expense_summa = divide(currency, exchange_rate , ex_sum )
        
        if not switchOnOff:
            expense = Expense.objects.create(
                expense_type=expense_type,
                currency=currency,
                expense_summa=expense_summa,
                exchange_rate=exchange_rate,
            )
            expense.containers.set(checked_items)  
            expense.save() 
            print(expense.containers, 'create')         
        else:
            expense = Expense.objects.create(
                    workers=workers,
                    currency=currency,
                    expense_summa=expense_summa,
                    exchange_rate=exchange_rate,
                )
            expense.containers.set(checked_items)  
            expense.save() 
          

        
        return JsonResponse({'status': 200, 'message': 'Expense created successfully'})
    
    
class EditWorkerView(View):
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
    def get(self,request):
        id = request.GET.get('id')
        worker = Worker.objects.filter(id=int(id)).first()
        worker.delete()
        
        return JsonResponse({'status': 200, 'message': 'Message deleted successfully'})


class SearchContainerView(View):
    def get(self, request):
        
        value =  request.GET.get('value')
        result = {
            'status':200,
            'data':[]
        }

        value = value.strip() if value else None
        
        query = Q(name__icontains=value) | Q(come_date__icontains=value)
        
        if value:
            containers = Container.objects.filter(query)
            
            
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
    def post(self,request):
        
        print()
        print(request.POST)
        print()
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
        
        return JsonResponse({'status': 200, 'message': 'Payment created successfully'})
    
class EditPaymentView(View):
    def post(self, request):
        payment_id = int(request.POST['payment_id'])
        payment_sum = int(request.POST['payment_sum'])
        currency_type = int(request.POST['currency_type'])
        exchange_rate = int(request.POST['exchange_rate'])
        
        
        payment = Payment.objects.filter(id=payment_id).first()
        container = payment.client_account.container_client
        last_client_info = payment.client_account
        last_payment_amount = payment.payment_amount
        last_currency = payment.currency
        last_sale_exchange_rate = payment.sale_exchange_rate
        
        if last_currency == 2:
            container.paid_amount -= (last_payment_amount/last_sale_exchange_rate)
            last_client_info.debt_uzs -= last_payment_amount
            last_payment_amount -= last_payment_amount
        if last_currency == 1:
            container.paid_amount -= last_payment_amount
            last_client_info.debt_usd -= last_payment_amount
            last_payment_amount -= last_payment_amount
            
        
        ###
        
        if currency_type == 2:
            container.paid_amount += (payment_sum / exchange_rate)
            last_client_info.debt_uzs += payment_sum
            
            last_payment_amount += payment_sum

        if currency_type == 1:
            container.paid_amount += payment_sum 
            last_client_info.debt_usd += payment_sum
            
            last_payment_amount += payment_sum

            
            
        last_client_info.save()
        last_payment_amount.save()
        container.save()
        payment.save()
        
        print()
        print(request.POST)
        print()
        
        return JsonResponse({'status': 200, 'message': 'Payment edited successfully'})
        
    

class GetClientDebt(View):
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

