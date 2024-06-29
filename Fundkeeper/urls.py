"""
URL configuration for Fundkeeper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from budget import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include("api.urls")),
    path('expense/create/',views.ExpenseCreateView.as_view(),name="expense-create"),
    path('expense/<int:pk>/update/',views.ExpenseUpdateView.as_view(),name="expense-update"),
    path('expense/<int:pk>/',views.ExpenseDetailView.as_view(),name="expense-detail"),
    path('expense/<int:pk>/delete/',views.ExpenseDeleteView.as_view(),name="expense-delete"),
    path('income/create/',views.IncomeCreateView.as_view(),name="income-create"),
    path('income/<int:pk>/update/',views.IncomeUpdateView.as_view(),name="income-update"),
    path('income/<int:pk>/',views.IncomeDetailView.as_view(),name="income-detail"),
    path('income/<int:pk>/delete/',views.IncomeDeleteView.as_view(),name="income-delete"),
    path('expense/summary/',views.ExpenseSummaryView.as_view(),name="expense-summary"),
    path('income/summary/',views.IncomeSummaryView.as_view(),name="income-summary"),
    path('register/',views.SignUpView.as_view(),name="register"),
    path('',views.SignInView.as_view(),name="signin"),
    path('logout/',views.SignOutView.as_view(),name="signout"),
    path('dashboard/',views.DashboardView.as_view(),name="dashboard")

]
