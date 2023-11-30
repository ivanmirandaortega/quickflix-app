from operator import contains
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from main_app.models import GENRES, Movie, Review
from .forms import ReviewForm
from django.contrib.auth.models import User



S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'myimagebucket28'

def search_movies(request):
  if request.method == "POST":
    searched = request.POST['searched']
    movies = Movie.objects.filter(genre__icontains=searched)
    return render(request,
    'movies/search_movies.html',
    {'searched': searched,
    'movies': movies})
  
  else:
    return render(request,
    'movies/search_movies.html',
    {})


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# Add the following import
from django.http import HttpResponse

# Define the home view
def home(request):
  return render(request,'home.html')



def movies_index(request):
  movies = Movie.objects.all()
  return render(request, 'movies/index.html', {'movies': movies})

class MovieCreate(LoginRequiredMixin,CreateView):
  model = Movie
  fields = ['name', 'description', 'genre']
  
  # This inherited method is called when a
  # valid cat form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)


@login_required
def add_review(request, movie_id):
  # if request.method == "POST":
  #   
	# create a ModelForm Instance using the data in the request
  form = ReviewForm(request.POST)

	# validate
  if form.is_valid():
    user = request.user
    
  
		# do somestuff
		# creates an instance of out review to be put in the database

  new_review = form.save(commit=False)
  new_review.movie_id = movie_id  
  new_review.user = user
  new_review.save() 
    

  return redirect('detail', movie_id=movie_id)

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)  

    if request.method == 'POST':         # If method is POST,
        review.delete()                     # delete the review.
        return redirect('/movies/')             # Finally, redirect to the homepage.

    return render(request, 'review_delete.html', {'review': review})
    # If method is not POST, render the default template.
    # *Note*: Replace 'template_name.html' with your corresponding template name.
  
def review_update(request, pk):
    context = {}
    review = get_object_or_404(Review, pk=pk)
    form = ReviewForm(request.POST or None, instance = review)
    if form.is_valid():
      form.save()
      return redirect('/movies/')


    context["form"] = form

    return render(request, 'review_update.html', {'review': review})




def assoc_review(request, movie_id, review_id):
  Movie.objects.get(id=movie_id).reviews.add(review_id)
  return redirect('detail', movie_id=movie_id)

class ReviewDetail(LoginRequiredMixin,CreateView):
  model = Review
  fields = ['comment', 'recommend']



class ReviewUpdate(LoginRequiredMixin,UpdateView):
  model = Review
  fields = ['comment', 'recommend']

class ReviewDelete(LoginRequiredMixin,CreateView):
  model = Review
  fields = ['comment', 'recommend']
  success_url = '/movies/'

def movies_detail(request, movie_id):
  

    movie = Movie.objects.get(id=movie_id)
    # create an instance of ReviewForm
    review_form = ReviewForm()
    favorite = bool
    if movie.favorites.filter(id=request.user.id).exists(): #checks if the user's id exists and see if they have added the movie to their favorites page
      favorite = True
    return render(request, 'movies/detail.html', {'movie': movie, 'review_form': review_form, 'favorite': favorite
    
    })
    
#this renders the favorites page
@login_required
def favorites(request): 
    new = Movie.newmanager.filter(favorites=request.user) #this filters newmanager inside of the Movie model; returns the data returned from the database 
    return render(request, 'movies/favorites.html', {'favorites': favorites, 'new': new}) #pass in variables for the favorites template


@login_required
def add_to_favorites(request, id):
    #the get_object_or_404 is a Django shortcut that calls get() on a model manager,
    #but it gives Http404 to return the standard error page
    movie = get_object_or_404(Movie, id=id) #pass in the Movie model and the id of the movie
    if movie.favorites.filter(id=request.user.id).exists(): #checks to see if the user id exists inside of the favorites field in the Movie model
        movie.favorites.remove(request.user) #if it exists, then remove it 
    else:
        movie.favorites.add(request.user) #else, add the id of user 
    return redirect('/favorites/') #redirect to the favorites page
    
    
