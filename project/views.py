from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import User, Category, Expense, Budget
from .forms import UserForm, CategoryForm, ExpenseForm, BudgetForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


def hello_page(request):
    return render(request, 'project/hello_page.html')

# User registration (as you already implemented)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after successful registration
            login(request, user)

            # Redirect to the home page after login
            return redirect('project:home')
    else:
        form = UserCreationForm()

    return render(request, 'project/register.html', {'form': form})


# User login view using Django's built-in LoginView
class CustomLoginView(LoginView):
    template_name = 'project/login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('project/home.html', kwargs={'pk': self.object.pk})


# User logout view using Django's built-in LogoutView
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('project:home')


def home(request):
    """Home page view for the finance tracker application"""
    return render(request, 'project/home.html')


class CategoryListView(ListView):
    model = Category
    template_name = 'project/categories.html'
    context_object_name = 'categories'


class ExpenseReportView(ListView):
    model = Expense
    template_name = 'project/expense_report.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_filter = self.request.GET.get('category')
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')

        if category_filter:
            queryset = queryset.filter(category__name=category_filter)
        if date_start and date_end:
            queryset = queryset.filter(date__range=[date_start, date_end])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_expenses'] = self.get_queryset().aggregate(
            total=Sum('amount'))['total'] or 0
        context['categories'] = Category.objects.all()
        return context


class BudgetAnalysisView(ListView):
    model = Budget
    template_name = 'project/budget_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budgets = Budget.objects.all()
        budget_analysis = []

        for budget in budgets:
            total_expenses = Expense.objects.filter(
                category=budget.category,
                date__range=[budget.start_date, budget.end_date]
            ).aggregate(total=Sum('amount'))['total'] or 0

            budget_analysis.append({
                'budget': budget,
                'total_expenses': total_expenses,
                'remaining_budget': budget.remaining_budget,
                'overspent': total_expenses > budget.total_budget
            })

        context['budget_analysis'] = budget_analysis
        return context
    

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'project/add_expense.html'
    success_url = reverse_lazy('project/expense_list')  # Redirect after successful form submission

    def form_valid(self, form):
        # Ensure the expense is associated with the logged-in user
        form.instance.account = self.request.user  # Set the user to the logged-in user
        form.instance.paid_by = self.request.user  # Assuming the user who created the expense is the one who paid
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Expense'
        return context


