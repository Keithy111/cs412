# blog/views.py
# views to show the blog application
from typing import Any
import random
from django.shortcuts import render, redirect
from django.urls import reverse  ## NEW

from . models import * 
from . forms import * ## NEW
from django.views.generic import ListView, DetailView, CreateView 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login ## NEW

# class-based view
class ShowAllView(ListView):
    '''A view to show all Articles.'''

    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

    def dispatch(self, *args, **kwargs):
        '''
        implement this method to add some tracing
        '''
        print(f"self.request.user={self.request.user}")
        # delegate to superclass version
        return super().dispatch(*args, **kwargs)

class RandomArticleView(DetailView):
    '''Show one article selected at random.'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = "article" # note the singular name

    ## AttributeError: Generic detail view RandomArticleView must be called with either an object pk or a slug in the URLconf.
    ## one solution: implement the get_object method.
    def get_object(self):
        '''Return the instance of the Article object to show.'''

        # get all articles
        all_articles = Article.objects.all() # SELECT *
        # pick one at random
        return random.choice(all_articles)
    

class ArticleView(DetailView):
    '''Show one article by its primary key.'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = "article" # note the singular name


class CreateCommentView(LoginRequiredMixin, CreateView):
    '''a view to show/process the create comment form:
    on GET: sends back the form
    on POST: read the form data, create an instance of Comment; save to database; ??
    '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    # what to do after form submission?
    def get_success_url(self) -> str:
        '''return the URL to redirect to after sucessful create'''
        #return "/blog/show_all"
        #return reverse("show_all")
        return reverse("article", kwargs=self.kwargs)
    
    def form_valid(self, form):
        '''this method executes after form submission'''

        print(f'CreateCommentView.form_valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        # find the article with the PK from the URL
        # self.kwargs['pk'] is finding the article PK from the URL
        article = Article.objects.get(pk=self.kwargs['pk'])

        # attach the article to the new Comment 
        # (form.instance is the new Comment object)
        form.instance.article = article

        # delegaute work to the superclass version of this method
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        build the template context data --
        a dict of key-value pairs.'''

        # get the super class version of context data
        context = super().get_context_data(**kwargs)

        # find the article with the PK from the URL
        # self.kwargs['pk'] is finding the article PK from the URL
        article = Article.objects.get(pk=self.kwargs['pk'])

        # add the article to the context data
        context['article'] = article

        return context

class CreateArticleView(LoginRequiredMixin, CreateView):
    '''View to create a new Article instance.'''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def form_valid(self, form):
        '''Add some debugging statements.'''
        print(f'CreateArticleView.form_valid: form.cleaned_data={form.cleaned_data}')

        # find which user is logged in
        user = self.request.user
        print(f'CreateArticleView:form_valid() user={user}')
        # attach the user to the new article instance
        form.instance.user = user

        # delegate work to superclass
        return super().form_valid(form)

class RegistrationView(CreateView):
    '''Display and process the UserVreationForm for account registration.'''

    template_name = 'blog/register.html'
    form_class = UserCreationForm


    def dispatch(self, *args, **kwargs):
        '''Handle the User creation process.'''

        # we handle the HTTP POST request
        if self.request.POST:
            
            print(f"self.request.POST={self.request.POST}")
            # reconstruct the UserCreationForm from the HTTP POST
            form = UserCreationForm(self.request.POST)
            # print(f'form={form}')
            if not form.is_valid():
                print(f'form.errors={form.errors}')
                # let's the CreateView superclass handle this problem!
                return super().dispatch(*args, **kwargs)

            # save the new User object
            user = form.save() # creates a new instance of User object in the database
            print(f"RegistrationView.dispatch: created user {user}")

            # log in the User
            login(self.request, user)
            print(f"RegistrationView.dispatch, user {user} is logged in.")

            ## mini_fb note: attach user to Profile creation form before saving.

            # redirect the user to some page view...
            return redirect(reverse('all'))

        # let the superclass CreateView handle the HTTP GET request:
        return super().dispatch(*args, **kwargs)