from django.db import models

# Create your models here.
class Movies(models.Model):
    show_id = models.CharField(unique=True,max_length=6,primary_key=True)
    type = models.CharField(max_length=8)
    title = models.CharField(unique=True,max_length=255)
    director = models.CharField(max_length=255,null=True)
    cast = models.CharField(max_length=555,null=True)
    country = models.CharField(max_length=255,null=True)
    date_added = models.CharField(max_length=255,null=True)
    release_year = models.IntegerField()
    age_rating = models.CharField(max_length=10,null=True)
    duration = models.CharField(max_length=12,null=True)
    listed_in = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=555,null=True)


    def __str__(self):
        return f"{self.title} ({self.release_year}) - {self.director}"
    class Meta:
        db_table = 'movies'