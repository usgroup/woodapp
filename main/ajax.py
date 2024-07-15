from django.views import View
from django.http import JsonResponse
from .models import ProductSize,Container, Product
from datetime import datetime
from .others_func import metr_to_cube

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
        
            
            
        return JsonResponse({'message': 'Prodcut Info updated successfully',"data":data})


       
class DeleteProduct(View):
    def post(self, request):
        product_id = int(request.POST['product_id'])
        
        Product.objects.filter(id=product_id)[0].delete()
        
        data = {
            "product_id":product_id
        }
        
        return JsonResponse({'message': 'Prodcut deleted successfully',"data":data})
        