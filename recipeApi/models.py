from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Recipe(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    recipeName = models.CharField(max_length= 100)
    recipeDescrip = models.TextField()
    recipeImg = models.ImageField(upload_to= "recipe")