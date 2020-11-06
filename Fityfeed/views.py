from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from .filters import fooditemFilter

from django.http import HttpResponseNotFound
# Create your views here.



@login_required(login_url='login')
@admin_only
def home(request):
    breakfast=Category.objects.filter(name='breakfast')[0].fooditem_set.all()[:5]
    lunch=Category.objects.filter(name='lunch')[0].fooditem_set.all()[:5]
    dinner=Category.objects.filter(name='dinner')[0].fooditem_set.all()[:5]
    snacks=Category.objects.filter(name='snacks')[0].fooditem_set.all()[:5]
    customers=Customer.objects.all()
    context={'breakfast':breakfast,
              'lunch':lunch,
              'dinner':dinner,
              'snacks':snacks,
              'customers':customers,
              'list_of_all': [breakfast, lunch, dinner, snacks],
              'list_of_name': ['breakfast', 'lunch', 'dinner', 'snacks'],
            }
    return render(request,'main.html',context)

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def fooditem(request):
    breakfast=Category.objects.filter(name='breakfast')[0].fooditem_set.all()
    bcnt=breakfast.count()
    lunch=Category.objects.filter(name='lunch')[0].fooditem_set.all()
    lcnt=lunch.count()
    dinner=Category.objects.filter(name='dinner')[0].fooditem_set.all()
    dcnt=dinner.count()
    snacks=Category.objects.filter(name='snacks')[0].fooditem_set.all()
    scnt=snacks.count()
    context={'breakfast':breakfast,
              'bcnt':bcnt,
              'lcnt':lcnt,
              'scnt':scnt,
              'dcnt':dcnt,
              'lunch':lunch,
              'dinner':dinner,
              'snacks':snacks,
            }
    return render(request,'fooditem.html',context)


def createfooditemadd(request):
    return render(request,'createfooditem1.html')


@login_required(login_url='login')
def createfooditem(request, catogary):
    if catogary =='dinner' or catogary == 'breakfast' or catogary == 'snacks' or catogary == 'lunch':
        form = fooditemForm()
        if request.method == 'POST':
            form = fooditemForm(request.POST)
            if form.is_valid():
                name = request.POST.get('name')
                carbohydrate = request.POST.get('carbohydrate')
                fats = request.POST.get('fats')
                protein = request.POST.get('protein')
                calorie = request.POST.get('calorie')
                u = Fooditem.objects.create(name= name, carbohydrate=carbohydrate, fats=fats, protein=protein, calorie=calorie)
                cate = Category.objects.get(name=catogary)
                users = Customer.objects.get(name=request.user)
                u.category.add(cate)
                u.customer.add(users)
                u.save()

                return redirect('/')
        else:
            context={'form':form, 'catogary': catogary}
       
    
        return render(request,'createfooditem.html',context)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@unauthorized_user
def registerPage(request):
    form=createUserForm()
    if request.method=='POST':
        form=createUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            user=form.save()
            Customer.objects.create(user=user, name=username,email=email)
            messages.success(request,'Account created for '+username)                    
            return redirect('login')
    context={'form':form}
    return render(request,'register.html',context)

@unauthorized_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is invalid')
    return render(request,'login.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def addFooditem(request):
    login_user=request.user
    if request.method=="POST":
        s = request.POST.get('s')
        if s:
            u = UserFooditem.objects.create()
            fooditems = Fooditem.objects.get(name=s)
            user = Customer.objects.get(user=login_user)
            u.customer.add(user)
            u.fooditem.add(fooditems)
            u.save()
            return redirect('/user')
        else:
            fooditems=Fooditem.objects.filter(customer__name=login_user)
            context={'fooditems':fooditems}
            return render(request,'addUserFooditem.html',context)
    else:
        fooditems=Fooditem.objects.filter(customer__name=login_user)
        context={'fooditems':fooditems}
        return render(request,'addUserFooditem.html',context)


@login_required(login_url='login')
def usersPage(request):
    user=request.user  
    cust=user.customer
    fooditems=Fooditem.objects.filter(customer__name=user)
    myfilter = fooditemFilter(request.GET,queryset=fooditems)
    fooditems=myfilter.qs
    total=UserFooditem.objects.all()
    myfooditems=total.filter(customer=cust)
    cnt=myfooditems.count()
    querysetFood=[]
    for food in myfooditems:
        querysetFood.append(food.fooditem.all())
    finalFoodItems=[]
    for items in querysetFood:
        for food_items in items:
            finalFoodItems.append(food_items)
    totalCalories=0
    for foods in finalFoodItems:
        totalCalories+=foods.calorie
    CalorieLeft=2000-totalCalories
    context={'CalorieLeft':CalorieLeft,'totalCalories':totalCalories,'cnt':cnt,'foodlist':finalFoodItems,'fooditem':fooditems,'myfilter':myfilter}
    return render(request,'user.html',context)











