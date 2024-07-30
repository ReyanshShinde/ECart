from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login,logout
from ecommapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.
def home(request):
    #return HttpResponse("<i>this is home page</i>")
    context={}
    context['name']="john"
    context['age']=10
    context['x']=10
    context['y']=20
    context['l']=[1,2,3,4]
    context['products']=[
     {'id':1,'name':'samsung','cat':'mobile','price':20000},
     {'id':2,'name':'jeans','cat':'cloth','price':500},
     {'id':3,'name':'adidas shoes','cat':'shoes','price':2000},
     {'id':4,'name':'vivo','cat':'mobile','price':15000}
    ]
    if context['x']>context['y']:
        res="x is greater"
    else:
        res="y is greater"
    return render(request,'home.html',context)
def about(request):
    return HttpResponse("<b>this is about page</b>")
def contact(request,a,b):
    print("a:",a)
    print(type(a))
    if int(a)>int(b):
        print(a,"is gretaer")
        res="a is greater"
    else:
        print(b,"is gretaest number")
        res="b is greater"
    return HttpResponse("<h1>this is a contact page</h1>"+res)
#class based views
class SimpleView(View):
    def get(self,request):
        return HttpResponse("hello from simple views")
def index(request):
    # userid=request.user.id
    # print("id logged in user:",userid)
    #print("Result:",request.user.is_authenticated)
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    print(p[0])
    print(p[0].name)
    print(p[0].price)
    print(p[1])
    print(p[1].price)
    print(p[1].pdetails)
    context['products']=p
    return render(request,'index.html',context)
def catfilter(request,cv):
    # print(cv)
    # print(type(cv))
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    #return HttpResponse("category value:"+cv)
    return render(request,"index.html",context)
def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=Product.objects.filter(is_active=True).order_by(col)
    #print(p)
    context={}
    context['products']=p
    return render(request,"index.html",context)
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    # print(min)
    # print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1&q2&q3)
    #print(p)
    context={}
    context['products']=p
    #return HttpResponse("values fetched")
    return render(request,"index.html",context)
def user_login(request):
    context={}
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pass']
        print(u)
        print(p)
        if u=="" or p=="":
            context['errmsg']="fields cannot empty"
            return render(request,'login.html',context)
        else:
            a=authenticate(username=u,password=p)
            # print(a)
            # print(a.username)
            # print(a.is_superuser)
            if a is not None:
                login(request,a)#start session and store id logged in user in session
                return redirect('/index')
            else:
                context['errmsg']="invalid username and password"
                return render(request,"login.html",context)
                #return HttpResponse("in else part")
    else:
        return render(request,'login.html')
def user_logout(request):
    logout(request)
    return redirect('/index')
def register(request):
    context={}
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pass']
        cp=request.POST['cpass']
        print(u)
        print(p)
        print(cp)
        if u=="" or p=="" or cp=="":
            context['errmsg']="field cannot be empty"
            return render(request,"register.html",context)
        elif p!=cp:
             context['errmsg']="password ans confrm passowrd did not match"
             return render(request,"register.html",context)
        else:
            try:
                u=User.objects.create(username=u,email=u)
                u.set_password(p)
                u.save()
                context['success']="user created successfully"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="user with same username alerady exist"
                return render(request,"register.html",context)
        return HttpResponse("user created successfully")
    return render(request,'register.html')
def product_detail(request,pid):
    p=Product.objects.filter(id=pid)
    #print(p)
    context={}
    context['products']=p
    return render(request,"product_detail.html",context)
def addtocart(request,pid):
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        # print(u)
        # print(u[0])
        # print(u[0].email)
        # print(u[0].username)
        p=Product.objects.filter(id=pid)
        # print(p)
        # print(p[0].name)
        # print(p[0].price)
        #check product exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1&q2)
        #print(c)
        n=len(c)
        #print("length:",n)
        context={}
        context['products']=p
        if n==1:
            context['msg']="product already exist in cart!!"
            return render(request,'product_detail.html',context)
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            
            #context={}
            #context['products']=p
            context['success']="product added successfully to cart!!"
            return render(request,"product_detail.html",context)
    else:
        return redirect('/login')
def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    #print(c)
    print(type(qv))
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/cart')
def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    # print(c)
    # print(c[0])
    # print(c[0].uid.username)
    # print(c[0].uid.email)
    # print(c[0].pid)
    # print(c[0].pid.name)
    # print(c[0].pid.price)
    #print(c[0].pid.name)
    s=0
    n=len(c)
    for x in c:
        # print(x)
        # print(x.pid.price)
        s=s+x.pid.price*x.qty
    context={}
    context['products']=c
    context['total']=s
    context['np']=n
    return render(request,"cart.html",context)
def remove(request,pid):
    c=Cart.objects.filter(id=pid)
    print(c)
    c.delete()
    return redirect('/cart')
def place_order(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    print(c)
    oid=random.randrange(1000,9999)
    print("order id:",oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    n=0
    for x in orders:
        # print(x)
        # print(x.pid.price)
        s=s+x.pid.price*x.qty
        n=n+x.qty
    context={}
    context['products']=orders
    context['total']=s
    context['np']=n
    return render(request,"place_order.html",context)
    #return HttpResponse("data is shifted")
def makepayment(request):
    #import razorpay
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_qPpA776V9DCblP", "TWcWQeLgGmHfG66yYcv7tzhJ"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    #return HttpResponse("in make payment page")
    return render(request,'pay.html',context)
def sendusermail(request):
    uemail=request.user.email
    print("*****",uemail)
    send_mail(
    "ECart7to9 placed successfully",
    "Order details are:",
    "i.am.shulker@gmail.com",
    [uemail],
    fail_silently=False,
    )
    return HttpResponse("Mail send successfully")
