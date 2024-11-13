# Author: Keith Yeung 
# Email: keithy@bu.edu 
# voter_analytics/views.py
# This file contains view functions and classes to handle requests and display voter data.

from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q
from datetime import date  
from django.db.models import Count
import plotly.express as px
from plotly.offline import plot


# Create your views here.

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html' 
    context_object_name = 'voters'
    paginate_by = 100  
    
    # Display only relevant fields
    def get_queryset(self) -> QuerySet:
      '''Return a filtered queryset of Voters based on search parameters.'''
      
      queryset = super().get_queryset()
      filters = {}

      # Filter by party affiliation if provided
      party_affiliation = self.request.GET.get('party_affiliation')
      if party_affiliation:
          filters['party_affiliation'] = party_affiliation

      # Filter by minimum date of birth
      min_dob = self.request.GET.get('min_dob')
      if min_dob:
          filters['date_of_birth__gte'] = date(int(min_dob), 1, 1)

      # Filter by maximum date of birth
      max_dob = self.request.GET.get('max_dob')
      if max_dob:
          filters['date_of_birth__lte'] = date(int(max_dob), 12, 31)

      # Filter by voter score if provided
      voter_score = self.request.GET.get('voter_score')
      if voter_score:
          filters['voter_score'] = int(voter_score)

      # Filter election participation based on query parameters
      election_fields = {
          'v20state': 'v20state',
          'v21town': 'v21town',
          'v21primary': 'v21primary',
          'v22general': 'v22general',
          'v23town': 'v23town'
      }
      
      # Use Q objects to dynamically add election participation filters
      election_query = Q()
      for param, field in election_fields.items():
          if self.request.GET.get(param) == 'true':
              election_query &= Q(**{field: True})
      
      queryset = queryset.filter(**filters).filter(election_query)

      return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = range(1913, 2006)
        context['voter_scores'] = range(1, 6)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        return context
    
class ShowVoterDetailView(DetailView):
    '''View to display a single Voter record.'''
    model = Voter
    template_name = 'voter_analytics/show_voter.html'
    context_object_name = 'voter'

class VoterGraphsView(ListView): 
    ''' A view to show the graphing data for voters '''

    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self) -> QuerySet:
      '''Return a filtered queryset of Voters based on search parameters.'''
      
      queryset = super().get_queryset()
      filters = {}

      party_affiliation = self.request.GET.get('party_affiliation')
      if party_affiliation:
          filters['party_affiliation'] = party_affiliation

      min_dob = self.request.GET.get('min_dob')
      if min_dob:
          filters['date_of_birth__gte'] = date(int(min_dob), 1, 1)

      max_dob = self.request.GET.get('max_dob')
      if max_dob:
          filters['date_of_birth__lte'] = date(int(max_dob), 12, 31)

      voter_score = self.request.GET.get('voter_score')
      if voter_score:
          filters['voter_score'] = int(voter_score)

      election_fields = {
          'v20state': 'v20state',
          'v21town': 'v21town',
          'v21primary': 'v21primary',
          'v22general': 'v22general',
          'v23town': 'v23town'
      }
      
      election_query = Q()
      for param, field in election_fields.items():
          if self.request.GET.get(param) == 'true':
              election_query &= Q(**{field: True})
      
      queryset = queryset.filter(**filters).filter(election_query)

      return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Get birth year histogram
        context['birth_year_histogram'] = self.create_birth_year_histogram(queryset)

        # Get party affiliation pie chart
        context['party_affiliation_pie'] = self.create_party_affiliation_pie(queryset)

        # Get election participation bar chart
        context['election_participation_histogram'] = self.create_election_participation_histogram(queryset)

        # Additional context data
        context['years'] = range(1913, 2006)
        context['voter_scores'] = range(1, 6)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        
        return context

    def create_birth_year_histogram(self, queryset):
        # Get the birth years from the queryset
        birth_years = queryset.values_list('date_of_birth', flat=True)
        birth_years = [dob.year for dob in birth_years]
        # Create the histogram plot
        fig = px.histogram(x=birth_years, nbins=20, labels={'x': 'Year of Birth'}, title="Distribution of Voters by Year of Birth")
        return plot(fig, output_type='div')

    def create_party_affiliation_pie(self, queryset):
        # Get party affiliation counts
        party_counts = queryset.values('party_affiliation').annotate(count=Count('party_affiliation'))
        # Create the pie chart plot
        fig = px.pie(party_counts, names='party_affiliation', values='count', title="Voters by Party Affiliation", width=600, height=600)
        return plot(fig, output_type='div')

    def create_election_participation_histogram(self, queryset):
        # Elections list
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        # Calculate the participation counts
        participation_counts = {election: queryset.filter(**{election: True}).count() for election in elections}
        # Create the bar chart plot
        fig = px.bar(x=list(participation_counts.keys()), y=list(participation_counts.values()), labels={'x': 'Election', 'y': 'Count'}, title="Voters by Election Participation")
        return plot(fig, output_type='div')
