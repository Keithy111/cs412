# Author: Keith Yeung 
# Email: keithy@bu.edu 
# project/forms.py
# This module defines forms for handling the project application, 

from django import forms
from .models import Profile, Category, Expense, Budget
from django.core.exceptions import ValidationError
from django.utils import timezone

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name', 'last_name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'date', 'paid_by']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'})
        }

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)  # Get 'profile' from kwargs, remove it from kwargs
        super().__init__(*args, **kwargs)

        if profile:
            # Filter categories based on the logged-in user's profile
            self.fields['category'].queryset = Category.objects.filter(profile=profile)

        if profile:
            # Set 'paid_by' field to the logged-in user (this won't be editable)
            self.fields['paid_by'].initial = profile  # Set initial value to logged-in user
            self.fields['paid_by'].widget = forms.HiddenInput()  # Hide the field in the form


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'total_budget', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'total_budget': forms.NumberInput(attrs={'step': '0.01'})
        }

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)  # Get 'profile' from kwargs, remove it from kwargs
        super().__init__(*args, **kwargs)

        if profile:
            # Filter categories based on the logged-in user's profile
            self.fields['category'].queryset = Category.objects.filter(profile=profile)