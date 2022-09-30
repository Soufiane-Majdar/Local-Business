from datetime import date
from django.db import models

# Create your models for csv data :
# "Name","Fulladdress",Street,Municipality,Categories,Phone,"Phones",Review Count,Average Rating,"Review URL",Google Maps URL,Latitude,Longitude,Website,Domain,"Opening hours",Featured image

# Choices for status
STATUS = (
    #default=0
    (0,"New"),
    (1,"Onhold"),
    (2,"In Progress"),
    (3,"Completed"),
    (4,"Canceled"),
    (5,"Rejected"),
    (6,"Accepted"),
    (7,"No Rsponse"),
    )

# name categories status phone phones website domain opening_hours date_added
# fulladdress street municipality   google_maps_url latitude longitude 
# review_count average_rating review_url 

class Busines(models.Model):
    name = models.CharField(max_length=250,unique=True)   # 
    fulladdress = models.CharField(max_length=250,blank=True,null=True)
    street = models.CharField(max_length=250,blank=True,null=True)
    municipality = models.CharField(max_length=250,blank=True,null=True)
    categories = models.CharField(max_length=250,blank=True,null=True)#
    phone = models.CharField(max_length=250,blank=True,null=True)#
    phones = models.CharField(max_length=250,blank=True,null=True)#
    review_count = models.CharField(max_length=250,blank=True,null=True)
    average_rating = models.CharField(max_length=250,blank=True,null=True)
    review_url = models.CharField(max_length=250,blank=True,null=True)
    google_maps_url = models.CharField(max_length=250,blank=True,null=True) 
    latitude = models.CharField(max_length=250,blank=True,null=True)
    longitude = models.CharField(max_length=250,blank=True,null=True)
    website = models.CharField(max_length=250,blank=True,null=True)#
    domain = models.CharField(max_length=250,blank=True,null=True)#
    opening_hours = models.CharField(max_length=250,blank=True,null=True)#
    featured_image = models.CharField(max_length=250,blank=True,null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.categories} | {self.average_rating} | {self.review_count} "


# class for wiches besness
class Favorite(models.Model):
    busines = models.ForeignKey(Busines, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.busines}"