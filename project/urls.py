from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'project'

urlpatterns = [
    path('', views.hello_page, name='hello_page'), 
    path('home/', views.home, name='home'), 
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='add_category'),  # Added trailing slash
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='edit_category'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('expenses/report/', views.ExpenseReportView.as_view(), name='expense_report'),
    path('expenses/add/', views.ExpenseCreateView.as_view(), name='add_expense'),  # Added trailing slash
    path('expenses/<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='edit_expense'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='delete_expense'),
    path('budgets/analysis/', views.BudgetAnalysisView.as_view(), name='budget_analysis'),
    path('create_budget/', views.BudgetCreateView.as_view(), name='create_budget'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
]
