from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


GENRES = (
   ('Romantic Comedy','Romantic Comedy'),
   ('Thrillers','Thrillers',),
   ('Drama','Drama'),
   ('Comedy','Comedy'),
   ('Documentary','Documentary'),
   ('Family','Family')
)



class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.CharField(max_length=250)
    movielink = models.CharField(max_length=250, default = '')
    movieposter = models.CharField(max_length=250)
    genre = models.CharField(
		max_length=15,
		#choices
		choices=GENRES,
		default=GENRES[0][0]
	)
    class NewManager(models.Manager): 
        def get_queryset(self):
            return super().get_queryset() 
    favorites = models.ManyToManyField(User, default=None, blank=True) 
    objects = models.Manager()
    newmanager = NewManager()
    def __str__(self):
        return f"The Movie {self.name} has id of {self.id}"

class Review(models.Model):
    comment = models.CharField(max_length=100)
    recommend = models.BooleanField('Would Recommend')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default = '1')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"The user {self.user} has id of {self.id} and {self.recommend}"

    def get_absolute_url(self):
        return reverse('review_detail', kwargs={'pk': self.id})