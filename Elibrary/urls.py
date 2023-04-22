"""Elibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse
from django.conf.urls.static import static
from django.conf import settings
from libraryhelper import views

urlpatterns = [
    path('admin/', admin.site.urls),

    ##USER URLS
    #TREATS ALL BUGS
    path('', views.index, name="index"),
    path('bookdetails/<int:book_pk>', views.bookdetail, name="bookdetail"),
    path('booksearch/', views.booksearch, name="booksearch"),
    path('booksearchresult/', views.searchresult, name="searchresult"),
    path('bookreservation/<int:book_pk>', views.bookreserve,name="bookreserve"),
    path('bookreservelist/<int:book_pk>', views.bookreservelist,name="bookreservelist"),
    path('bookcatalouge/<str:varone>/<str:vartwo>',views.bookcatalouge,name="bookcatalouge"),


    ##liberian URLS
    path('login/', views.login, name="login"),
    path('homepage/', views.home, name="home"),
    path('searchreservation/', views.searchreservation, name="searchreservation"),
    path('approve/', views.approve, name="approve"),
    path('approve/<int:approve_pk>', views.approvestudent, name="approvestudent"),
    path('approvereserve/<int:reserve_pk>', views.approvereserve, name="approvereserve"),
    path('overdue/', views.overdue, name="overdue"),
    path('searchoverdue/', views.searchoverdue, name="searchoverdue"),
    path('searchdefault/', views.searchdefault, name="searchdefault"),
    path('defaulters/', views.defaulters, name="defaulters"),
    path('viewdefaulters/<int:defaulter_pk>', views.viewdefaulters, name="viewdefaulters"),
    path('addbook/', views.addbook, name="addbook"),
    path('addcopy/', views.addcopy, name="addcopy"),

    #admin URLS UNTESTED URLS
    path('approvecopylist/', views.approvecopylist, name="approvecopylist"),
    path('approvebooklist/', views.approvebooklist, name="approvebooklist"),
    path('approvecopy/<int:copy_pk>', views.approvecopy, name="approvecopy"),
    path('approvebook/<int:copy_pk>', views.approvebook, name="approvebook"),
    
    path('addliberian/', views.addliberian, name="addliberian"),
    path('personalinfo/', views.personalinfo, name="personalinfo"),
    path('liberianlist/', views.liberianlist, name="liberianlist"),
    path('liberianinfo/', views.liberianinfo, name="liberianinfo"),
    path('makeadmin/', views.makeadmin, name="makeadmin"),
    path('deleteliberian/', views.deleteliberian, name="deleteliberian"),
    
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#To allow the url to matvh the patter when used in djangotemplates
url = reverse('bookcatalouge', args=['A','None'])