from django.db import models

# Create your models here.
class Movies(models.Model):
    show_id = models.CharField(unique=True,max_length=6,primary_key=True)
    type = models.CharField(max_length=8)
    title = models.CharField(unique=True,max_length=255)
    director = models.CharField(max_length=255)
    cast = models.CharField(max_length=555)
    country = models.CharField(max_length=255)
    date_added = models.CharField(max_length=255)
    release_year = models.IntegerField()
    age_rating = models.CharField(max_length=10)
    duration = models.CharField(max_length=12)
    listed_in = models.CharField(max_length=255)
    description = models.CharField(max_length=555)


    def __str__(self):
        return f"{self.title} ({self.release_year}) - {self.director}"
    class Meta:
        db_table = 'movies'