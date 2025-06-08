from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('base/',views.base,name="base"),
    path('reg/',views.reg,name="reg"),
    path('login/',views.login_view,name="login"),
    path('adminlogin/',views.adminlogin,name="adminlogin"),
    path('userlogin/',views.userlogin,name="userlogin"),
    path('fooddatabase/',views.fooddatabase,name="fooddatabase"),
    path('mealplanning/',views.mealplanning,name="mealplanning"),
    path('goals/',views.goals,name="goals"),
    path('mealentry/',views.mealentry,name="mealentry"),
    path('nutritionalanalysis/', views.nutritionalanalysis, name='nutritionalanalysis'),
    path('summary/', views.summary, name='summary'),
    path('admins/',views.admins,name="admins"),
    path('update/<int:id>/',views.update,name="update"),
    path('delete/<int:id>/',views.delete,name="delete"),
    path('addfood/',views.addfood,name="addfood"),
    path('user/',views.user,name="user"),
    path('update_goal/<int:goal_id>/', views.update_goal, name='update_goal'),
    path('delete_goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path('signout/',views.signout,name="signout"),
    path('update_profile/',views.update_profile,name="update_profile"),
]