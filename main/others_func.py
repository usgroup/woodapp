from .models import *
from django.http import JsonResponse
from collections import defaultdict



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


def transform_order_data(data):
    """
    Transforms raw POST data into a structured format.
    """
    orders = defaultdict(dict)
    
    for key, value in data.items():
        if key.startswith('order_list['):
            # Extract order_id and field_name from the key
            parts = key.split('][')
            order_id = parts[0].replace('order_list[', '')
            field_name = parts[1].replace(']', '')
            
            # Store the value in the appropriate place
            orders[order_id][field_name] = value
    
    # Convert defaultdict to list of dictionaries
    return list(orders.values())

def process_order_data(request):
    """
    Processes the POST data and returns the transformed data as JSON.
    """
    if request.method == 'POST':
        raw_data = request.POST.dict()  # Convert QueryDict to regular dict
        transformed_data = transform_order_data(raw_data)
        
        return transformed_data
    
    
def divide(currency, exchange_rate , ex_sum ):
    
    if currency == 1:
        return ex_sum
    if currency == 2:
        division_sum = (ex_sum / exchange_rate)
        
    
    
    return division_sum

