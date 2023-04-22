from django.db import models
import datetime
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy 


uuser = get_user_model()
# Create your models here.
class Book(models.Model):
    booktitle = models.CharField(max_length=100,unique=True)
    bookimg =  models.ImageField(default='./kraft-notebook-with-elastic-band-2542530__340.jpg',upload_to="elibrary/bookimages")
    authors = models.CharField(blank=True,max_length=200)
    edition = models.CharField(blank=True,max_length=100)
    booktype = models.CharField(blank=True,max_length=20)
    deptclass = models.CharField(blank=True,max_length=100)
    year = models.DateField(blank=True)
    isbn = models.CharField(blank=True,max_length=100)
    aisle = models.CharField(blank=True,max_length=100)
    description = models.TextField()
    approve = models.BooleanField(default=False)
    dateadded = models.DateTimeField(auto_now_add=True)
    pdf_available = models.BooleanField(default=True,null=False)
    pdf_file = models.FileField(blank=True, upload_to='elibrary/pdfs/')
    popular = models.IntegerField()

    
    def __str__(self):
        return (self.booktitle)


class Copy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    copyname = models.CharField(max_length=100,unique=True)
    available = models.BooleanField(default=False,null=False)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.copyname},{self.book}"


class Reservee(models.Model):
        book = models.ForeignKey(Book, on_delete=models.CASCADE)
        surname = models.CharField(max_length=100)
        matric = models.CharField(max_length=100,unique=True)
        firstname = models.CharField(max_length=100)
        department = models.CharField(max_length=100)
        school = models.CharField(max_length=100)
        datecreated = models.DateTimeField(auto_now_add=True)


        def __str__(self):
            return (self.matric)


class Loan(models.Model):
        copy = models.ForeignKey(Copy, on_delete=models.CASCADE)
        matric = models.CharField(max_length=100)
        firstname = models.CharField(max_length=100)
        surname = models.CharField(max_length=100)
        department = models.CharField(max_length=100)
        school = models.CharField(max_length=100)
        dateloaned = models.DateTimeField(auto_now_add=True)
        returndate = models.DateTimeField(blank=True,null=True)


        def __str__(self):
            return f"{self.matric},{self.copy}"


class Review(models.Model):
        matric = models.CharField(max_length=100,unique=True)
        totalloanbook= models.IntegerField()
        totalretbook = models.CharField(max_length=100)
        lstreturndate = models.DateTimeField(blank=True)


        def __str__(self):
            return (self.matric)


class Defaulters(models.Model):
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE)
    matric = models.CharField(max_length=100,unique=True)
    prior = models.IntegerField()
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    datereated = models.DateTimeField(auto_now_add=True)


class Liberian(models.Model):
    class Gender(models.TextChoices):
        Male = 'M', ('Male')
        Female = 'F', ('Female')

    user = models.OneToOneField(uuser, on_delete=models.CASCADE)
    dob = models.DateField()
    address = models.TextField(max_length=200,blank=True)
    bio = models.TextField(max_length=200,blank=True)
    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.Male,
    )
    nin = models.CharField(max_length=200,blank=True)
    isAdmin = models.BooleanField(default=False)
    profileimg =  models.ImageField(default='./blank-profile-picture-circle-hd.png',upload_to="libraryhelper/images")
    