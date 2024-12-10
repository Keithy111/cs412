from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import Profile, Category, Expense, Budget, User
from .forms import ProfileForm, CategoryForm, ExpenseForm, BudgetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from datetime import timedelta
import random


def hello_page(request):
    return render(request, 'project/hello_page.html')

def budget_analysis_view(request):
    budgets = Budget.objects.all()  # Or any filtering logic
    budget_analysis = []

    for budget in budgets:
        analysis = {
            'budget': budget,
            'total_expenses': budget.total_expenses,
            'remaining_budget': budget.remaining_budget,
            'overspent': budget.total_expenses > budget.total_budget,
        }
        budget_analysis.append(analysis)

    return render(request, 'project/budget_analysis.html', {'budget_analysis': budget_analysis})

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user first
            user = user_form.save()
            
            # Create profile with the saved user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Automatically log in the user after successful registration
            login(request, user)
            
            # Redirect to the home page after login
            return redirect('project:home')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'project/register.html', {
        'form': user_form,
        'profile_form': profile_form
    })


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
    # List of YouTube video URLs to display randomly
    video_urls = [
        "https://youtu.be/T_776Cwvejs?si=W14llzdnmyVQmmpu",  # Example video 1
        "https://youtu.be/IfpAjsytwy0?si=3qwttQbvsl_edTZt",   # Example video 2
        "https://youtu.be/NEzqHbtGa9U?si=9GagkrN5g6KRVfXq",
        "https://youtu.be/_vecpj_CRLw?si=zsQEXN0--OubwfGv",
        "https://youtu.be/N2aODJWw7Xw?si=Q0fIoSEzhcbJlDxg",
        "https://youtu.be/a-vmZpnpze0?si=UVa5krQHAhCBGf8Q"
    ]
    
    # Pick a random video URL
    random_video_url = random.choice(video_urls)

    # Extract the video ID for embedding
    video_id = random_video_url.split('youtu.be/')[1].split('?')[0]

    # Pass the video ID to the template
    return render(request, 'project/home.html', {'random_video_id': video_id})

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'project/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(profile=self.request.user.project_profile)

class ExpenseReportView(ListView):
    model = Expense
    template_name = 'project/expense_report.html'

    def get_queryset(self):
        profile = self.request.user.project_profile
        queryset = Expense.objects.filter(profile=profile)
        
        # Get filters from request
        category_filter = self.request.GET.get('category')
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')

        # Apply category filter
        if category_filter:
            queryset = queryset.filter(category__name=category_filter)
        
        # Apply date range filter
        if date_start and date_end:
            queryset = queryset.filter(date__range=[date_start, date_end])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.project_profile
        
        # Get categories associated with the user's profile
        context['categories'] = Category.objects.filter(profile=profile)

        # Calculate total expenses
        context['total_expenses'] = self.get_queryset().aggregate(
            total=Sum('amount'))['total'] or 0

        return context


class BudgetAnalysisView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'project/budget_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter budgets by the logged-in user's profile
        budgets = Budget.objects.filter(profile=self.request.user.project_profile)

        budget_analysis = []
        monthly_expenses = {}

        # Aggregate expenses for the last 365 days, done once here.
        expenses = Expense.objects.filter(profile=self.request.user.project_profile, date__gte=timezone.now() - timedelta(days=365))
        for expense in expenses:
            month = expense.date.strftime('%Y-%m')  # Format as 'YYYY-MM'
            monthly_expenses[month] = monthly_expenses.get(month, 0) + expense.amount

        # Iterate over budgets of the logged-in user only
        for budget in budgets:
            total_expenses = budget.calculate_total_expenses()
            budget.update_budget_metrics()
            budget_analysis.append({
                'budget': budget,
                'total_expenses': total_expenses,
                'remaining_budget': budget.remaining_budget,
                'overspent': budget.total_expenses > budget.total_budget,
            })

        context['budget_analysis'] = budget_analysis
        context['monthly_expenses'] = monthly_expenses
        return context


    
class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'project/add_expense.html'
    success_url = reverse_lazy('project:expense_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = self.request.user.project_profile  # Pass the logged-in user's profile to the form
        return kwargs

    def form_valid(self, form):
        try:
            # Attempt to retrieve the profile for the logged-in user
            profile = self.request.user.project_profile  
            
            # Associate the expense with the user's profile
            form.instance.profile = profile
            
            # # Associate the expense with the budget (assuming a "Transportation" category exists)
            # form.instance.budget = Budget.objects.get(profile=profile, category__name="Transportation")
            
        except ObjectDoesNotExist:
            form.add_error(None, "Profile does not exist for the logged-in user.")
            return self.form_invalid(form)

        # Call the parent method to save the expense
        response = super().form_valid(form)
        
        # # Update the budget after saving the expense
        # self.update_budget(self.object)
        
        return response

    def update_budget(self, expense):
        """
        Update the budget related to this expense.
        """
        budget = expense.budget  # Get the associated budget
        
        # Update the budget metrics
        budget.update_budget_metrics()
        
        # Save the updated budget with updated metrics
        budget.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Expense'
        return context

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    fields = ['category', 'amount', 'description', 'date']
    template_name = 'project/edit_expense.html'
    
    def get_success_url(self):
        return reverse_lazy('project:expense_report')

    def form_valid(self, form):
        # Ensure the expense is associated with the logged-in user's profile
        form.instance.profile = self.request.user.project_profile
        return super().form_valid(form)

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'project/delete_expense.html'
    
    def get_success_url(self):
        return reverse_lazy('project:expense_report')

    def get_object(self, queryset=None):
        expense = super().get_object(queryset)
        # Ensure the expense belongs to the logged-in user
        if expense.profile != self.request.user.project_profile:
            raise PermissionDenied
        return expense
    
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'project/add_category.html'
    success_url = reverse_lazy('project:categories')

    def form_valid(self, form):
        try:
            profile = self.request.user.project_profile  # Ensure the user has a profile
            form.instance.profile = profile  # Assign the profile to the budget instance
        except ObjectDoesNotExist:
            form.add_error(None, "Profile does not exist for the logged-in user.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Category'
        return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'project/edit_category.html'
    
    def get_success_url(self):
        return reverse_lazy('project:categories')  # Redirect to the category list view

    def form_valid(self, form):
        # Ensure the category is associated with the logged-in user's profile
        if form.instance.profile != self.request.user.project_profile:
            raise PermissionDenied
        return super().form_valid(form)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'project/delete_category.html'
    
    def get_success_url(self):
        return reverse_lazy('project:categories')  # Redirect to the category list view

    def get_object(self, queryset=None):
        category = super().get_object(queryset)
        # Ensure the category belongs to the logged-in user
        if category.profile != self.request.user.project_profile:
            raise PermissionDenied
        return category

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'project/create_budget.html'
    success_url = reverse_lazy('project:budget_analysis')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = self.request.user.project_profile  # Pass the logged-in user's profile to the form
        return kwargs

    def form_valid(self, form):
        try:
            profile = self.request.user.project_profile  # Ensure the user has a profile
            form.instance.profile = profile  # Assign the profile to the budget instance
        except ObjectDoesNotExist:
            form.add_error(None, "Profile does not exist for the logged-in user.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Budget'  # Set the title for the template
        return context

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'project/edit_budget.html'
    
    def get_success_url(self):
        return reverse_lazy('project:budget_analysis')  # Redirect to the budget list view

    def form_valid(self, form):
        # Ensure the budget is associated with the logged-in user's profile
        if form.instance.profile != self.request.user.project_profile:
            raise PermissionDenied
        return super().form_valid(form)

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'project/delete_budget.html'
    
    def get_success_url(self):
        return reverse_lazy('project:budget_analysis')  # Redirect to the budget list view

    def get_object(self, queryset=None):
        budget = super().get_object(queryset)
        # Ensure the budget belongs to the logged-in user
        if budget.profile != self.request.user.project_profile:
            raise PermissionDenied
        return budget

