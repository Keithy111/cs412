## blog/models.py
## define the data objects for our application 
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User ## NEW

# Create your models here.

class Article(models.Model):
  '''Encapsulate the idea of one Article by some author.'''

  # data attributes of a Article:
  user = models.ForeignKey(User, on_delete=models.CASCADE) ## NEW

  #data attributes of an Article
  title = models.TextField(blank=False)
  author = models.TextField(blank=False)
  text = models.TextField(blank=False)
  published = models.DateTimeField(auto_now=True)
  #image_url = models.URLField(blank=True) # url as a string
  image_file = models.ImageField(blank=True) # an actual image


  def __str__(self):
    '''Return a string representation of this object.'''

    return f'{self.title} by {self.author}'
  
  def get_comments(self):
    '''Return all of the comments about this article.'''
    comments = Comment.objects.filter(article=self)
    return comments

  # ... data attributes and other methods ...
  def get_absolute_url(self):
      '''Return the URL to display this Article.'''
      return reverse('article', kwargs={'pk':self.pk})

      
class Comment(models.Model):
    '''Encapsulate the idea of a Comment on an Article.'''
    
    # data attributes of a Comment:

    # model the 1 to many relationship with Article (foreign key)
    article = models.ForeignKey("Article", on_delete=models.CASCADE) ## if article gets deleted delete the comments as well
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'

