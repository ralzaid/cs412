from django.shortcuts import render
import random
from datetime import datetime, timedelta

dSpecial = [
    'Fatoush - $5.00',
    'Baba Ghanoush - $7.00',
    'Falafel - $6.00',
]

menu = {
    'Chicken Shawarma': 8.00,
    'Beef Shawarma': 8.00,
    'Hummus': 6.00,
    'Daily Special': 0.00,
}

def main(request):
    template_name = "restaurant/main.html"

    context = {
        'name': 'Sufra Mediterranean Food',
        'location': '52 Queensberry St, Boston, MA 02215',
        'hours': [
            'Sunday - Wednesday: 11:00 AM - 12:00 AM',
            'Thursday - Saturday: 11:00 AM - 1:30 AM',
        ],
        'photos': ['src/sufra.jpg'],
    }
    return render(request, template_name, context)

def order(request):
    template_name = "restaurant/order.html"
    
    daily_special = random.choice(dSpecial)
    
    special_name, special_price = daily_special.split(' - $')
    special_price = float(special_price)
    
    menu['Daily Special'] = special_price

    context = {
        'sName': special_name,
        'sPrice': special_price,
        'menu': menu
    }
    
    return render(request, template_name, context)


    

def confirmation(request):
    template_name = "restaurant/confirmation.html"
    if request.method == 'POST':

        order_items = request.POST.getlist('items')
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')
        customer_email = request.POST.get('email')
        special_instructions = request.POST.get('special_instructions')

        total = 0.0
        for i in order_items:
            total += menu.get(i, 0.0)

        minutes = random.randint(30, 60)
        readytime = datetime.now() + timedelta(minutes)

        context = {
            'order_items': order_items,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'total': total,
            'readytime': readytime.strftime("%I:%M %p")
        }
        return render(request, template_name, context)

    return render(request, template_name)
