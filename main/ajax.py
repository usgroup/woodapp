from django.views import View
from django.http import JsonResponse
from .models import ProductSize,Container, Product, Client, Order, OrderItem, ExpenseType, Expense
from datetime import datetime
from .others_func import metr_to_cube,process_order_data

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
        
        
        if currencyType == 1 and usd_currency <= 0:
            return JsonResponse(data={'status':400,'error_message': 'Valyuta kursni kiritishni unutdingiz !'})
        try:
            debt_check = request.POST['debt_check']
            if debt_check and client_id == 0:
                return JsonResponse(data={'status':400,'error_message': 'Nasiya savdoda mijoz kiritish muhim !'})
           
            if debt_check and client_id > 0:
                client = Client.objects.filter(id=client_id)[0]
                
                order = Order.objects.create(
                                customer=client,
                                currency=currencyType,
                                sale_exchange_rate=usd_currency,
                                total_summa=totalSumma,
                                debt_status=True,
                            )
                
            if currencyType == 1:
                client.debt_usd = totalSumma
            else:
                client.debt_uzs = totalSumma
                
            client.save()   
        except:
            pass
        
        order = Order.objects.create(
                currency=currencyType,
                sale_exchange_rate=usd_currency,
                total_summa=totalSumma,
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
                total_price=int(float(i['total_price'])),
            )
            
            new_qty = product.rest_qty - int(i['amount_sold'])
            product.rest_cube = metr_to_cube(product.product_size.product_size_x,product.product_size.product_size_y, product.product_size.product_size_z, new_qty)
            product.rest_qty = new_qty
            
            product.save()
            
        #message add 
        return JsonResponse({'status':200,'message': 'Product sale successfully'})
    
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

        