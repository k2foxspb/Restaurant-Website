from .models import *
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.views import View

class Order(View):
    def get(self, request, *args, **kwargs):
        appetizers = StarterMenu.objects.filter(starterOption='Starter')
        entres = MainMenu.objects.filter(mainOption='Main')
        desserts = DessertMenu.objects.filter(dessertOption='Dessert')
        drinks = DrinksMenu.objects.filter(drinksOption='Drink')
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
            'heros' : Hero.objects.all(),
            'links': Link.objects.all().first(),
            'footer': Footer.objects.all().first(),
        }
        return render(request, 'users/order.html', context)
    def post(self, request, *args, **kwargs):
        name =  request.POST['name']
        email =  request.POST['email']
        location =  request.POST['location']
        phone_number =  request.POST['phone_number']
        if(name and email and location and phone_number):
            app_order_items = {
                'items': []
            }
            main_order_items = {
                'items': []
            }
            dessert_order_items = {
                'items': []
            }
            drinks_order_items = {
                'items': []
            }
            app_items = request.POST.getlist('app_items[]')
            main_items = request.POST.getlist('main_items[]')
            dessert_items = request.POST.getlist('dessert_items[]')
            drink_items = request.POST.getlist('drink_items[]')
            for app_item in app_items:
                menu_item = StarterMenu.objects.get(pk__contains=int(app_item))
                key = 'app-items-' + (app_item)
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.starterContent,
                    'price': menu_item.starterPrice,
                    'amount': request.POST[key]
                }
                app_order_items['items'].append(item_data)
            for main_item in main_items:
                menu_item = MainMenu.objects.get(pk__contains=int(main_item))
                key = 'entre-items-' + (main_item)
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.mainContent,
                    'price': menu_item.mainPrice,
                    'amount': request.POST[key]
                }
                main_order_items['items'].append(item_data)
            for dessert_item in dessert_items:
                menu_item = DessertMenu.objects.get(pk__contains=int(dessert_item))
                key = 'dessert-items-' + (dessert_item)
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.dessertContent,
                    'price': menu_item.dessertPrice,
                    'amount': request.POST[key]
                }
                dessert_order_items['items'].append(item_data)
            for drink_item in drink_items:
                menu_item = DrinksMenu.objects.get(pk__contains=int(drink_item))
                key = 'drink-items-' + (drink_item)
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.drinksContent,
                    'price': menu_item.drinksPrice,
                    'amount': request.POST[key]
                }
                drinks_order_items['items'].append(item_data)
            
            price = 0
            app_item_ids = []
            main_item_ids = []
            dessert_item_ids = []
            drinks_item_ids = []
            for item in app_order_items['items']:
                price += (float((item['price'])[1:]) * int(item['amount']))
                for i in range(int(item['amount'])):
                    app_item_ids.append(item['id'])
            for item in main_order_items['items']:
                price += (float((item['price'])[1:]) * int(item['amount']))
                for i in range(int(item['amount'])):
                    app_item_ids.append(item['id'])
            for item in dessert_order_items['items']:
                price += (float((item['price'])[1:]) * int(item['amount']))
                for i in range(int(item['amount'])):
                    app_item_ids.append(item['id'])
            for item in drinks_order_items['items']:
                price += (float((item['price'])[1:]) * int(item['amount']))
                for i in range(int(item['amount'])):
                    app_item_ids.append(item['id'])
            
            order = OrderModel.objects.create(price=price)
            order.starterItems.add(*app_item_ids)
            order.mainItems.add(*main_item_ids)
            order.dessertItems.add(*dessert_item_ids)
            order.drinkItems.add(*drinks_item_ids)
            order.name = (name)
            order.email = (email)
            order.location = (location)
            order.phone = (phone_number)
          
            
            if(price == 0):
                appetizers = StarterMenu.objects.filter(starterOption='Starter')
                entres = MainMenu.objects.filter(mainOption='Main')
                desserts = DessertMenu.objects.filter(dessertOption='Dessert')
                drinks = DrinksMenu.objects.filter(drinksOption='Drink')
                context = {
                    'appetizers': appetizers,
                    'entres': entres,
                    'desserts': desserts,
                    'drinks': drinks,
                    'heros' : Hero.objects.all(),
                    'links': Link.objects.all().first(),
                    'footer': Footer.objects.all().first(),
                }
                messages.warning(request, 'Please choose an item')
                return render(request, 'users/order.html', context)
            else:
                
                order.save()  

                context = {
                'app_items': app_order_items['items'],
                'main_items': main_order_items['items'],
                'dessert_items': dessert_order_items['items'],
                'drink_items': drinks_order_items['items'],
                'price': price,
                'heros' : Hero.objects.all(),
                'links': Link.objects.all().first(),
                'footer': Footer.objects.all().first(),
                    
                }
                return render(request, 'users/order_confirmation.html', context)
        else:
            
                appetizers = StarterMenu.objects.filter(starterOption='Starter')
                entres = MainMenu.objects.filter(mainOption='Main')
                desserts = DessertMenu.objects.filter(dessertOption='Dessert')
                drinks = DrinksMenu.objects.filter(drinksOption='Drink')
                context = {
                    'appetizers': appetizers,
                    'entres': entres,
                    'desserts': desserts,
                    'drinks': drinks,
                    'heros' : Hero.objects.all(),
                    'links': Link.objects.all().first(),
                    'footer': Footer.objects.all().first(),
                }
                messages.warning(request, 'Please fill details')
                return render(request, 'users/order.html', context)
            

def home(request):
    context1 = {
        'heros' : Hero.objects.all(),
        'aboutUs': About.objects.all(),
        'whyUs': WhyUs.objects.all(),
        'footer': Footer.objects.all().first(),
        'location': Location.objects.all(),
        'openHours': OpeningHour.objects.all().first(),
        'email': Email.objects.all(),
        'call': Call.objects.all(),
        'starterMenu': StarterMenu.objects.all(),
        'mainMenu': MainMenu.objects.all(),
        'dessertMenu': DessertMenu.objects.all(),
        'drinksMenu': DrinksMenu.objects.all(),
        'testimonials': Testimonial.objects.all(),
        'events': Event.objects.all(),
        'specials': Special.objects.all(),
        'chefs':Chef.objects.all(),
        'specials': Special.objects.all(),
        'links': Link.objects.all().first()

    }    
    
    return render(request, 'restaurant/home.html',context1)


def reservation(request):
    
   
    if request.method == "POST":
        your_name = request.POST['name']
        your_phone = request.POST['phone']
        your_email = request.POST['email']
        date = request.POST['date']
        time = request.POST['time']
        number_of_people = request.POST['people']
        message = request.POST['message']
        
        reservation = "Name:" + your_name + " /n Phone:" + your_phone + "/n Email:" + your_email + "/n Date:" + date + "/n Time:" + time + " /n Number of People" + number_of_people + "/n Message:" + message
        send_mail(
            'Reservation Request',
            reservation,
            your_email,
            ['se.dagmawit.getachew@gmail.com'],
        )

        return render(request, 'restaurant/reservation.html', {
        'your_name':your_name,
        'your_phone':your_phone,
        'your_email':your_email,
        'date':date,
        'time':time,
        'number_of_people':number_of_people,
        'message':message, })
    else:
        return render(request, 'restaurant/home.html',{})

    

  
