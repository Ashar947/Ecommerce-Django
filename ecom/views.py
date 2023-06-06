from django.shortcuts import render  , redirect
from django.http import HttpResponse , HttpResponseRedirect
from .models import Category , Product , Cart , Order , user_table ,Wishlist
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , logout , authenticate
import ast
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template

def render_to_pdf(temp,dic={}):
    template = get_template(temp)
    html = template.render(dic)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

def prodpdf(request,id):
    try:
        prod = Product.objects.get(id=id)
    except:
        return HttpResponse("Error")
    data ={
        "prod_id" : prod.id,
        "prod_name":prod.Name,
        "prod_cat":prod.Category,
        "prod_date":prod.Publish_Date,
        "images":prod.Image.url,
        "prod_price":prod.Price,
    }
    pdf = render_to_pdf('ecom/prodviewpdf.html',data)
    if pdf:
        response = HttpResponse(pdf,content_type="application/pdf")
        return response
    return HttpResponse("Not Found")

path = "" 
# def base(request):
#     param = {}
#     cat = Category.objects.all()
#     param = {'data':cat}
#     return render(request,'ecom/base.html',param)
def index(request):
    cat = Category.objects.all()
    prod = Product.objects.all()
    # print(prod)
    # return HttpResponse("on")
    obj ={'Cats': cat , 'Prods':prod}
    # print(obj)
    return render(request,'ecom/index.html',obj)

def user_login(request):
    return render(request,'ecom/signin.html')

def handle_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email,password=password)
        if user is not None: 
            login(request,user)
            return HttpResponseRedirect('/ecom/')
        else:
            return HttpResponse("Invalid Credentials")
    else:
        return HttpResponse("Error CSRF")    

def user_signup(request):
    return render(request,'ecom/signup.html')

def user_create(request):
    if request.method == 'POST':
        # username = request.POST.get('UserName')
        first_name=request.POST.get('FirstName')
        last_name=request.POST.get('LastName')
        email=request.POST.get('email')
        password=request.POST.get('password')
        address=request.POST.get('address')
        country=request.POST.get('country')
        city=request.POST.get('city')
        contact_number=request.POST.get('ContactNumber')
        user = User.objects.create_user(email,email,password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        reg = user_table(user=user,address=address,contact_number=contact_number,country=country,city=city) #register_table is the name of the model class
        reg.save()
        return HttpResponseRedirect("/ecom/signin/")
    else:
        return HttpResponse('Error !! Please retry again')
    

def user_profile(request):
    if request.user.is_authenticated:
        param = {}
        data = user_table.objects.get(user__id=request.user.id)
        param = {'info':data}
        return render(request,'ecom/profile.html',param)
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/ecom/')
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)

def cart(request):
    if request.user.is_authenticated:
        total = 0
        user = User.objects.get(id=request.user.id)
        print(f'User : {user}')
        data = user_table.objects.get(user__id=request.user.id)
        obj = Cart.objects.filter(User = user.username)    
        for item in obj:
            sum = (item.Quantity) * (item.Price_Cart)
            total = total + sum
        param = {'cart':obj,'number':len(Cart.objects.all()), 'total_price':total,'info':data}   
        return render(request,'ecom/cart.html', param)
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)



def checkout(request):
    if request.user.is_authenticated:
        

            # for y in range(qty):
            #     
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)     
            prod_list = []
            carts = Cart.objects.filter(User=user.username)
            for x in carts:
                qty = x.Quantity
                if qty==1:
                    prod_list.append(x.prod_id)
                else:
                    for i in range(qty):
                        prod_list.append(x.prod_id)
            cust_name = request.POST.get('customer_name') + " " + request.POST.get('customer_lastname')
            cust_email = request.POST.get('customer_email')
            cust_phone = request.POST.get('customer_phone')
            cust_address = request.POST.get('customer_address')
            payment = request.POST.get('pay')
            if payment=="COD":
                card_number = 0
                card_exp= ""
                card_cvv = 0
            if payment=="Card":
                card_number = request.POST.get("cardnum")
                print(card_number)
                card_exp= request.POST.get("cardexp")
                card_cvv = request.POST.get("cardcvv")
            save =Order.objects.create(user=user.username,customer_name=cust_name,customer_email=cust_email,customer_contact=cust_phone,customer_address=cust_address,items=prod_list , Card_Nummber = card_number , Card_Expiration = card_exp , Card_Cvv = card_cvv , Payment_Method = payment)
            save.save()
            params = {'id': save.id}    
            Cart.objects.filter(User=user.username).delete()   
            return render(request , 'ecom/checkout.html',params)
        else :
            return redirect("/ecom/")
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)

def cat(request,id):
    path = request.path
    category = Category.objects.get(id=id)
    prod_cat = Product.objects.filter(Category =id)
    # print(prod_cat)
    cat = {'cats':category,'prods':prod_cat}
    # print(cat)
    return render(request,'ecom/category.html',cat)


def addtocart(request,id):
    # print(path)
    a=request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        username = user.username
        prod = Product.objects.get(id=id)
        try:
            cart = Cart.objects.get(User=username,prod_id=prod.id)
            if cart:
                quantity = cart.Quantity + 1
                total_price = cart.Price_Cart * quantity
                cart.Quantity = quantity 
                cart.sum = total_price 
                cart.save()
                return HttpResponseRedirect(f'{a}#{id}')
        except Cart.DoesNotExist:
            Cart.objects.create(User=username,prod_id=prod.id,Name_Cart=prod.Name,Quantity=1,sum=prod.Price ,Category_Cart=prod.Category,Price_Cart=prod.Price,Image_Cart=prod.Image)
            # return HttpResponseRedirect("/ecom/#",id)
            return HttpResponseRedirect(f'{a}#{id}') 
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)

def cartdel(request,id):
    if request.user.is_authenticated:
        Cart.objects.get(id=id).delete()
        return HttpResponseRedirect('/ecom/cart/')
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)



def wishlist(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        obj = Wishlist.objects.filter(user=user.username)
        data = {'obj':obj}
        return render(request,'ecom/wishlist.html',data)
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)

def addtowishlist(request,id):
    a=request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        userobj = User.objects.get(id=request.user.id)
        prod = Product.objects.get(id=id)
        saved = Wishlist(user=userobj.username, Name=prod.Name,Category=prod.Category,Price=prod.Price,Image=prod.Image)
        saved.save()
        return HttpResponseRedirect(f'{a}#{id}')
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)

def searchbar(request):
    param = {}
    path = request.path
    if request.method=='GET':
        query = request.GET.get('searchbar')
        prod = Product.objects.filter(Name__icontains=query)
        param = {'Prods':prod}
        return render(request,'ecom/search.html',param)

    
def viewupdateprofile(request):
    if request.user.is_authenticated:
        param={}
        data = user_table.objects.get(user__id=request.user.id)
        param = {'info':data}
        return render(request,'ecom/updateprofile.html',param)
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)

def password(request):
    if request.user.is_authenticated:
        return render(request,'ecom/changepass.html')
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)
def update_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(id=request.user.id)
            old = request.POST.get('oldpass')
            check = user.check_password(old)
            new = request.POST.get('NewPass')
            confirm = request.POST.get('confrimpass')
            if check==True:
                if new==confirm:
                    user.set_password(new)
                    user.save()
                else:
                    return HttpResponse("Pass doesnot match")    
            else:
                return HttpResponse("Old pass is not correct")

            return HttpResponseRedirect('/ecom/signin/')
        else:
            return HttpResponse("Error retry again")
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)

def update_profile(request):
    if request.user.is_authenticated:
        user_data = user_table.objects.get(user__id=request.user.id)
        if request.method == 'POST':
            first_name=request.POST.get('FirstName')
            last_name=request.POST.get('LastName')
            email=request.POST.get('email')
            address=request.POST.get('address')
            country=request.POST.get('country')
            city=request.POST.get('city')
            contact_number=request.POST.get('ContactNumber')
            usr = User.objects.get(id=request.user.id)
            usr.first_name=first_name
            usr.last_name=last_name
            # usr.username=email
            # usr.email=email
            usr.save()
            user_data.contact_number=contact_number
            user_data.address=address
            user_data.country=country
            user_data.city=city
            user_data.save()
            return HttpResponseRedirect('/ecom/userprofile/')
        else:
            return HttpResponse("Error try again please")
        
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)
        
def orderhistory(request):
    if request.user.is_authenticated:
        param={}
        user=User.objects.get(id=request.user.id)
        orders = Order.objects.filter(user=user.username)
        param={"data":orders}
        return render(request,'ecom/orderhistory.html',param)
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)
        


def vieworder(request,id):
    if request.user.is_authenticated:
        param={}
        order = Order.objects.get(id=id)
        ini_list=order.items
        final_list = ast.literal_eval(ini_list)
        print(final_list)
        newlist = [] # empty list to hold unique elements from the list
        duplist = [] # empty list to hold the duplicate elements from the list
        for i in final_list:
            if i not in newlist:
                newlist.append(i)
            else:
                duplist.append(i)
        prod = Product.objects.filter(id__in=final_list)
        prod2 = Product.objects.filter(id__in=duplist)
        total=0
        for x in prod:
            total = total + x.Price
        for y in prod2:
            total = total + y.Price

        method = False
        if (order.Payment_Method == "Card"):
            method = True
        print(method)
        param = {'data':prod,'Order':order,'data2':prod2,'total':total,'show':method}
        return render(request,'ecom/vieworder.html',param)
    else:
        param={}
        param={"data":'You need to be Logged in '}
        return render(request,'ecom/error.html',param)



    



def decqty_cart(request,id):
    user=User.objects.get(id=request.user.id)
    cart = Cart.objects.get(id=id)
    dec = cart.Quantity - 1
    # 
    if dec<=0:
        Cart.objects.filter(User=user.username,id=id).delete()
    else:
        cart.Quantity = dec
        cart.save()
    return HttpResponseRedirect("/ecom/cart/#cart")


def incqty_cart(request,id):
    cart = Cart.objects.get(id=id)
    inc = cart.Quantity + 1
    cart.Quantity = inc
    cart.save()
    return HttpResponseRedirect("/ecom/cart/#cart")