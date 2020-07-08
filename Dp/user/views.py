from django.shortcuts import render
from .models import Product, Contact, Order, Orderupdate
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from PayTm import Checksum
# Create your views here.

MERCHANT_KEY = 'wAwNeIGinzsVfIjG';

def index(request):
    products = Product.objects.all()
    print(products)
    params = {'product': products}
    return render(request, 'user/index.html', params)


def search(request):
    #return HttpResponse("search page")
    return render(request, 'user/search.html')

def about(request):
    return render(request, 'user/about.html')

def contact(request):
    thank = False
    if request.method == "POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'user/contact.html', {'thank': thank})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Order(items_json=items_json, name=name, amount=amount, email=email, address=address, city=city,
                        state=state, zip_code=zip_code, phone=phone)
        order.save()
        # update = OrderUpdate(order_id=order_id, update_desc="the oreder has been placed")
        # update.save()
        print(items_json)
        thank = True
        id = order.order_id
        
        # return render(request, 'user/checkout.html', {'thank': thank, 'id': id})
        param_dict = {
        "MID": "uRKQis55188856454271",
        "ORDER_ID": str(order.order_id),
        "CUST_ID": email,
        "TXN_AMOUNT": str(amount),
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": "WEBSTAGING",
        "CALLBACK_URL" : "http://ec2-13-126-17-214.ap-south-1.compute.amazonaws.com/user/handlerequest/",
    }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'user/paytm.html', {'param_dict': param_dict})
    return render(request, 'user/checkout.html')

def productView(request, myid):
    product = Product.objects.filter(product_name=myid)
    return render(request, 'user/prodview.html', {'product':product})

@csrf_exempt

def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]= form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('oder successful')
        else:
            print('oder was not successful'+ response_dict['RESPMSG'])
    return render(request, 'user/paymentstatus.html', {'response': response_dict})
