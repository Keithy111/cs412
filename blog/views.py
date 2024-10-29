# blog/views.py
# define the views for the blog app
from django.shortcuts import render
from django.urls import reverse
from typing import Any

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView ## NEW
from .models import * ## import the models (e.g., Article)
from .forms import * ## import the forms (e.g., CreateCommentForm)
from .forms import CreateArticleForm, CreateCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW


import random

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article # the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # context variable to use in the template

    def dispatch(self, request):
        '''add this method to show/debug logged in user'''
        print(f"Logged in user: request.user={request.user}")
        print(f"Logged in user: request.user.is_authenticated={request.user.is_authenticated}")
        return super().dispatch(request)
    
    ## show all users in views

class RandomArticleView(DetailView):
    '''Display one Article selected at Random'''
    model = Article # the model to display
    template_name = "blog/article.html"
    context_object_name = "article"

    # AttributeError: Generic detail view RandomArticleView must be called with either an object pk or a slug in the URLconf.
    # one solution: implement get_object method
    def get_object(self):
        '''Return one Article chosed at random.'''

        # explicitly add an error to generate a call stack trace:
        # y = 3 / 0

        # retrieve all of the articles
        all_articles = Article.objects.all()
        # pick one at random
        article = random.choice(all_articles)
        return article

class ArticleView(DetailView):
    '''Display one Article selected by PK'''
    model = Article # the model to display
    template_name = "blog/article.html"
    context_object_name = "article"

class CreateCommentView(CreateView):
    '''
    A view to create a Comment on an Article.
    on GET: send back the form to display
    on POST: read/process the form, and save new Comment to the database
    '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        # get the context data from the sueprclass
        context =  super().get_context_data(**kwargs)

        # find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])
        
        # add the Article referred to by the URL into this context
        context['article'] = article
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        # return 'show_all' # a valid URL pattern
        # return reverse('show_all') # look up the URL called "show_all"

        # find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])
        return reverse('article', kwargs={'pk':article.pk})
        # return reverse('article', kwargs=self.kwargs)

    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''

        print(f'CreateCommentView.form_valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        # find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])

        # attach this Article to the instance of the Comment to set its FK
        form.instance.article = article # like: comment.article = article

        # delegate work to superclass version of this method
        return super().form_valid(form)

class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to create a new Article and save it to the database.'''
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self) -> str:
        '''Return the Url required for login'''
        return reverse('login')
    
    def form_valid(self, form):
        '''Handle the form submission to create a new Article object.'''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')

        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")

        # attach user to form instance (Article object):
        form.instance.user = user
        return super().form_valid(form)