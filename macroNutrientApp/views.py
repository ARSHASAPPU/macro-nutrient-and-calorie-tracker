from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
import sweetify
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, date


# Create your views here.
def base(request):
    return render(request,"base.html")
def home(request):
    return render(request,"home.html")

def reg(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        role=request.POST.get("role")
        usersave=User.objects.create_user(name=name,email=email,password=password,role = role)
        if role=="user":
            return redirect('login')
        else :
            return redirect("adminlogin")
    return render(request,"reg.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,username=email,password=password)

        if user:
            if user.role == 'user':
                login(request,user)
                return redirect("userlogin")
            else:
                error_message = 'You do not have permission to access this page.'
                return render(request, "login.html", {'error_message': error_message})
        
        else:
            error_message = 'Invalid email or password.'
            return render(request, "login.html", {'error_message': error_message})
    return render(request, "login.html")

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,username=email,password=password)

        if user:
            if user.role == 'admin':
                login(request,user)
                return redirect("admins")
            else:
                error_message = 'You do not have permission to access this page.'
                return render(request, "adminlogin.html", {'error_message': error_message})
        
        else:
            error_message = 'Invalid email or password.'
            return render(request, "adminlogin.html", {'error_message': error_message})
    return render(request, "adminlogin.html")

def admins(request):
    # Filter to exclude admin and superuser roles
    details = User.objects.exclude(role__in=['admin', 'superuser'])
    mealentries = MealEntry.objects.all()
    fooddetails = Food.objects.all()
    goals = GoalSetting.objects.all()
    for goal in goals:
        print(goal.__dict__)
    
    # Include passwords (not recommended)
        user_data = [{'name': user.name, 'email': user.email, 'password': user.password} for user in details]
    
    return render(request, "admins.html", {'details': user_data, 'mealentries': mealentries, 'fooddetails': fooddetails, 'goals': goals, 'is_admin': True})

@login_required
def mealentry(request):
    # Check if the user has a goal set
   
    goal_setting = GoalSetting.objects.filter(user=request.user).first()
    if not goal_setting:
        sweetify.error(request, 'You need to set a goal before adding a meal entry!', button='Go to Goals')
        return redirect('goals')  # Redirect to the goals page

    
    if request.method == 'POST':
        food_name = request.POST.get('food')
        quantity = request.POST.get('quantity')
        date = request.POST.get('date')
        try:
            food = Food.objects.get(name=food_name)
        except Food.DoesNotExist:
            messages.error(request, 'Food item not found.')
            return redirect('mealentry')

        meal_entry = MealEntry(user=request.user, food=food, quantity=quantity, date=date)
        meal_entry.save()
        print('final', meal_entry)
        sweetify.success(request, 'Meal entry submitted successfully!')
        return redirect('mealentry')
    else:
        foods = Food.objects.all()
        # goals = GoalSetting.objects.filter(user=request.user)
        return render(request, 'mealentry.html', {'foods': foods})

def fooddatabase(request):
    foods = Food.objects.all()
    return render(request, 'fooddatabase.html', {'foods': foods})

def update(request,id):
    u=Food.objects.filter(id=id)
    if request.method=="POST":
        name=request.POST['name']
        calories=request.POST['calories']
        proteins=request.POST['proteins']
        carbs=request.POST['carbs']
        fat=request.POST['fat']
        Food.objects.filter(id=id).update(name=name,calories=calories,protein=proteins,carbs=carbs,fat=fat)
        return redirect('admins')
    return render(request,"update.html",{'u':u})

def delete(request,id):
    emp=Food.objects.get(id=id)
    emp.delete()
    return redirect('admins')

def addfood(request):
    if request.method=="POST":
        name=request.POST['name']
        calories=request.POST['calories']
        proteins=request.POST['proteins']
        carbs=request.POST['carbs']
        fat=request.POST['fat']
        foodsave=Food(name=name,calories=calories,protein=proteins,carbs=carbs,fat=fat)
        foodsave.save()
        return redirect('admins')
    return render(request,"addfood.html")

    
@login_required
def nutritionalanalysis(request):
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    try:
        meal_entries = MealEntry.objects.filter(user=request.user)

        for entry in meal_entries:
            total_calories += entry.food.calories * entry.quantity
            total_protein += entry.food.protein * entry.quantity
            total_carbs += entry.food.carbs * entry.quantity
            total_fat += entry.food.fat * entry.quantity
    except MealEntry.DoesNotExist:
        meal_entries = []

    context = {
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fat': total_fat,
    }
    return render(request, 'nutritionalanalysis.html', context)


@login_required
def summary(request):
    total_meals = 0
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    meal_entries = MealEntry.objects.filter(user=request.user)

    total_meals = meal_entries.count()
    for entry in meal_entries:
        total_calories += entry.food.calories * entry.quantity
        total_protein += entry.food.protein * entry.quantity
        total_carbs += entry.food.carbs * entry.quantity
        total_fat += entry.food.fat * entry.quantity

    # Retrieve the date from GoalSettings
    
    goal_setting = GoalSetting.objects.filter(user=request.user).first()
    goal_date_str = goal_setting.timeframe if goal_setting else None
    goal_date = datetime.strptime(goal_date_str, '%Y-%m-%d').date() if goal_date_str else None  # Updated format
    days_left = (goal_date - date.today()).days if goal_date else None

    context = {
        'total_meals': total_meals,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fat': total_fat,
        'goal_date': goal_date,
        'days_left': days_left,
    }

    return render(request, 'summary.html', context)
    
@login_required
def user(request):
    f = User.objects.filter(id=request.user.id)
    return render(request, "user.html", {'f': f})


def userlogin(request):
    return render(request,"userlogin.html")


@login_required
def mealplanning(request):
    meal_plans = MealPlanning.objects.filter(user=request.user)
    if request.method == 'POST':
        meal = request.POST.get('meal')
        food = request.POST.get('food')
        quantity = request.POST.get('quantity')
        date = request.POST.get('date')

        meal_plan = MealPlanning(user=request.user, meal=meal, food=food, quantity=quantity, date=date)
        meal_plan.save()
        return HttpResponse('Meal planned successfully')
    return redirect('mealplanning')


@login_required
def goals(request):
    if request.method == 'POST':
        goal_type = request.POST.get('goaltype')
        target_metrics = request.POST.get('targetmetrics')
        timeframe = request.POST.get('timeframe')

        # Check if the user already has a goal
        existing_goal = GoalSetting.objects.filter(user=request.user).first()
        if existing_goal:
            sweetify.warning(request, "You already have a goal set. Please edit or delete the existing goal before adding a new one.")
            return redirect('goals')  # Redirect back to the goals page

        # If no existing goal, save the new goal
        goal_setting = GoalSetting(user=request.user, goal_type=goal_type, target_metrics=target_metrics, timeframe=timeframe)
        goal_setting.save()
        sweetify.success(request, "Goal set successfully!")
        return redirect('goals')
    else:
        # Fetch existing goals for the user
        existing_goals = GoalSetting.objects.filter(user=request.user)
        return render(request, 'goals.html', {'existing_goals': existing_goals})


@login_required
def update_goal(request, goal_id):
    goal = GoalSetting.objects.get(id=goal_id, user=request.user)
    if request.method == 'POST':
        goal.goal_type = request.POST.get('goaltype')
        goal.target_metrics = request.POST.get('targetmetrics')
        goal.timeframe = request.POST.get('timeframe')
        goal.save()
        sweetify.success(request, "Goal updated successfully!")
        return redirect('goals')
    return render(request, 'goals.html', {'goal': goal})

@login_required
def delete_goal(request, goal_id):
    goal = GoalSetting.objects.get(id=goal_id, user=request.user)
    goal.delete()
    sweetify.success(request, "Goal deleted successfully!")
    return redirect('goals')
       
        
def signout(request):
    logout(request)
    return redirect("home")

@login_required
def update_profile(request):
    if request.method == "POST":
        name = request.POST.get("name")  # This should match the name in the input field
        email = request.POST.get("email")
        password = request.POST.get("password")

        print('Name:', name)  # Debugging output

        user = request.user
        user.name = name  # Update the first name
        user.email = email

        if password:
            user.set_password(password)  # Securely update the password
            update_session_auth_hash(request, user)  # Keep the user logged in

        user.save()
        sweetify.success(request, "Profile updated successfully!")
        return redirect("user")  # Redirect to profile page after update

    return render(request, "user.html")
