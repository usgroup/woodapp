from .models import *


def metr_to_cube(x,y,z, qty):
    qty = qty
    
    x = x / 1000
    y = y / 1000
    z = z
    
    volume = (x * y * z) * qty
    
    return volume


def calc_end_write(request, pk):
    select_size_id = int(request.POST['select_size'])
    product_qty = int(request.POST['product_qty'])
    come_cost = int(request.POST['come_cost'])
    
    product_size = ProductSize.objects.filter(id=select_size_id)[0]
    
    container = Container.objects.filter(id=int(pk))[0]
    
    volume = metr_to_cube(product_size.product_size_x, product_size.product_size_y, product_size.product_size_z, product_qty)
 
    print()
    print(volume)
    print()
    
    Product.objects.create(
        product_container=container,
        product_size=product_size,
        product_qty=product_qty,
        come_cost=come_cost,
        product_cube=volume,
        rest_cube=volume,
        rest_qty=product_qty,
    )
    
    return True


