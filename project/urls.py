from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'project'

urlpatterns = [
    path('', views.hello_page, name='hello_page'), 
    path('home/', views.home, name='home'), 
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('expenses/report/', views.ExpenseReportView.as_view(), name='expense_report'),
    path('add_expense/', views.ExpenseCreateView.as_view(), name='add_expense'),
    path('budgets/analysis/', views.BudgetAnalysisView.as_view(), name='budget_analysis'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
]