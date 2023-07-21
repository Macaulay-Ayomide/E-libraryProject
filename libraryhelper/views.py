from curses import longname
from django.shortcuts import redirect, render, get_object_or_404
from .models import Book, Copy, Liberian, Reservee, Loan, Review, Defaulters
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, tzinfo,time
from .forms import BookForm, ReserveForm,LoanForm,DefaulterForm,CopyForm,LiberianForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django import template
from .forms import BookForm
from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError



# Create your views here.
###USERS METHOD
def index(request):
    book = Book.objects.all().order_by('-dateadded')
    approvelist = Loan.objects.all().order_by('-dateloaned')
    elapse = datetime.now()-timedelta(days = 1)
    overduelist = Loan.objects.filter(dateloaned__lt= elapse)
    return render(request,"libraryhelper/index.html",{'book':book,'approvelist':approvelist,'overduelist':overduelist,'elapse':elapse})

def bookcatalouge(request,varone,vartwo):
    if vartwo != "None":
        items = Book.objects.filter(approve='True',booktitle__startswith=varone,deptclass=vartwo,booktype="book").order_by('booktitle') 
        return render(request, 'libraryhelper/bookcatalog.html', {'items': items,'varone':varone,'vartwo':vartwo})
    else:
        items = Book.objects.filter(approve='True',booktitle__startswith=varone,booktype="book").order_by('booktitle') 
        return render(request, 'libraryhelper/bookcatalog.html', {'items': items,'varone':varone,'vartwo':vartwo})
    
def journalcatalouge(request,varone,vartwo):
    if vartwo != "None":
        items = Book.objects.filter(approve='True',booktitle__startswith=varone,deptclass=vartwo,booktype="journal").order_by('booktitle') 
        return render(request, 'libraryhelper/journalcatalouge.html', {'items': items,'varone':varone,'vartwo':vartwo})
    else:
        items = Book.objects.filter(approve='True',booktitle__startswith=varone,booktype="journal").order_by('booktitle') 
        return render(request, 'libraryhelper/journalcatalouge.html', {'items': items,'varone':varone,'vartwo':vartwo})
    
def papercatalouge(request,varone,vartwo):
    if vartwo != "None":
        items = Book.objects.filter(approve='True',booktitle__startswith=varone,deptclass=vartwo,booktype="paper").order_by('booktitle') 
        return render(request, 'libraryhelper/papercatalouge.html', {'items': items,'varone':varone,'vartwo':vartwo})
    else:
        items = Book.objects.filter(approve='True',booktitle__startswith=varone,booktype="paper").order_by('booktitle') 
        return render(request, 'libraryhelper/papercatalouge.html', {'items': items,'varone':varone,'vartwo':vartwo})

def allcatalouge(request,varone,vartwo):
    if vartwo != "None":
        items = Book.objects.filter(approve='True',booktitle__startswith=varone,deptclass=vartwo).order_by('booktitle') 
        return render(request, 'libraryhelper/allcatalouge.html', {'items': items,'varone':varone,'vartwo':vartwo})
    else:
        items = Book.objects.filter(approve='True',booktitle__startswith=varone).order_by('booktitle') 
        return render(request, 'libraryhelper/allcatalouge.html', {'items': items,'varone':varone,'vartwo':vartwo})

def booksearch(request):
    return render(request,"libraryhelper/booksearch.html")


def bookdetail(request,book_pk):
    bookdetail = get_object_or_404(Book, pk=book_pk)
    return render(request,"libraryhelper/bookdetail.html",{'book':bookdetail})

def bookreservelist(request, book_pk):
    reservelist = Reservee.objects.filter(book=book_pk,datecreated__gte=(datetime.now()-timedelta(days = 7)))
    defaulters_list = Defaulters.objects.all()
    return render(request,"libraryhelper/reservelist.html",{'reservelist':reservelist,'defaulters_list':defaulters_list})


def bookreserve(request, book_pk):
    if request.method == 'GET':
        copy = Copy.objects.filter(book=book_pk,available=True)
        if copy.count() > 1:
            return render(request,"libraryhelper/bookreserve.html",{'copy':copy})
        else:
            return render(request,"libraryhelper/bookreserve.html",{'copy':copy,'error':'error'})
    elif request.method == 'POST':
        if Reservee.objects.filter(matric=request.POST['Matric']).count() >= 3:
            error = "You can't make a reservation for more than three books in a week"
            return render(request,"libraryhelper/bookreserve.html",{'error':error})
        elif Reservee.objects.filter(matric=request.POST['Matric'],book=book_pk):
            error = "You can't make more than one reservation for the same book"
            return render(request,"libraryhelper/bookreserve.html",{'error':error})
        #check for blank
        if (request.POST['Firstname'] == "") | (request.POST['Surname'] == "") | (request.POST['Matric'] == ""):
            error = "You didn't fill in your first name"
            return render(request,"libraryhelper/bookreserve.html",{'error':error})
        #Create an object for reserve
        book=Book.objects.get(pk=book_pk)
        reservee = Reservee.objects.create(book=book,surname=request.POST['Surname'],firstname=request.POST['Firstname'],matric=request.POST['Matric'],department=request.POST['Department'],school=request.POST['School'])
        reservee.save()
        return redirect('bookreservelist',book_pk=book_pk)
    return render(request,"libraryhelper/bookdetail.html",{'book':bookdetail})



def searchresult(request):
    bookname = request.GET.get('bookname', '').strip()
    searchby = request.GET.get('searchby', '')
    department = request.GET.get('department', '')
    booktype = request.GET.get('booktype', '')

    if not bookname:
        message = "You didn't input any name to search for"
        return render(request, "libraryhelper/booksearch.html", {'message': message})

    booklist = Book.objects.filter(Q(booktitle__icontains=bookname) | Q(authors__icontains=bookname),approve=True)
    
    if booklist.count() < 1:
        message = "The book is not available for the time being in the library"
        return render(request, "libraryhelper/booksearch.html", {'message': message})

    if searchby == "Book Title":
        booklist = booklist.filter(booktitle__icontains=bookname,approve=True)
  
    if department and department != 'None':
        booklist = booklist.filter(deptclass=department,approve=True)

    if booktype and booktype != 'None':
        booklist = booklist.filter(booktype=booktype,approve=True)

    if booklist:
        return render(request, "libraryhelper/booksearchresult.html", {'booklist': booklist})
    
    message = "The application is unable to understand your query"
    return render(request, "libraryhelper/booksearch.html", {'message': message})


###Liberian methods
def loginuser(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("hhhhh")
            return redirect('logout')
        else:
            return render(request,'libraryhelper/login.html',{'form':AuthenticationForm()})
    else:
        if request.method == 'POST':
            user = authenticate(request, username=request.POST['username'], password =request.POST['password'])
            if user is None:
                return render(request,'libraryhelper/login.html',{'form':AuthenticationForm(),'error':'Username and password did not match'})
            else:
                login(request, user)
                return redirect('home')


#@login_required
#{% if isAdmin %}
    # is_admin = False
    # if request.user.is_authenticated:
    #     is_admin = Liberian.objects.filter(user=request.user, isAdmin=True).exists()

@login_required
def home(request):
    reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 7)))
    defaulters_list = Defaulters.objects.all()
    admin = Liberian.objects.get(user=request.user)
    return render(request,"libraryhelper/home.html",{'reservelist':reservelist,'defaulters_list':defaulters_list,'admin':admin})


@login_required
def searchreservation(request):
    admin = Liberian.objects.get(user=request.user)
    if request.method == 'GET':
        if request.GET['searchname'] == "":
            message ="You didn't input any name to search for"
            reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
            return render(request,"libraryhelper/home.html",{'message':message,'reservelist':reservelist,'admin':admin})
    elif request.method == 'POST': 
        try:
            if request.POST['searchby'] == "Firstname":
                reservelist = Reservee.objects.filter(firstname__icontains=request.POST['searchname'])
                return render(request,"libraryhelper/home.html",{'reservelist':reservelist,'admin':admin})
            elif request.POST['searchby'] == "Surname":
                reservelist = Reservee.objects.filter(surname__icontains=request.POST['searchname'])
                return render(request,"libraryhelper/home.html",{'reservelist':reservelist,'admin':admin})
            elif request.POST['searchby'] == "School":
                reservelist = Reservee.objects.filter(school__icontains=request.POST['searchname'])
                return render(request,"libraryhelper/home.html",{'reservelist':reservelist,'admin':admin})
            elif request.POST['searchby'] == "Department":
                reservelist = Reservee.objects.filter(department__icontains=request.POST['searchname'])
                return render(request,"libraryhelper/home.html",{'reservelist':reservelist,'admin':admin})
            elif request.POST['searchby'] == "matric":
                reservelist = Reservee.objects.filter(matric__icontains=request.POST['searchname'])
                return render(request,"libraryhelper/home.html",{'reservelist':reservelist,'admin':admin})
        except MultiValueDictKeyError:
                if Loan.objects.filter(matric=request.POST['matric']).count() > 3:
                    message ="The student can't have more then three books"
                    return render(request,"libraryhelper/reservresult.html",{'message':message,'admin':admin})
                checker = Review.objects.filter(matric=request.POST['matric']).first()
                if checker:
                    if (checker.totalretbook /checker.totalloanbook) < 0.335 and  ((datetime.now()- checker.lstreturndate) < 30) :
                        message ="The student can't have a very low return rate"
                        return render(request,"libraryhelper/reservresult.html",{'message':message,'admin':admin})
                student = Reservee.objects.get(matric=request.POST['matric'])
                avail = Copy.objects.filter(book=student.book,available=True).first()
                if avail:
                    ovdate = datetime.now()
                    expdate = datetime.now()+ timedelta(days = 7)
                    ovdate = (datetime.now() - expdate).days
                    loan = Loan.objects.create(
                        copy=avail,
                        surname=request.POST['surname'],
                        firstname=request.POST['firstname'],
                        matric=request.POST['matric'],
                        department=request.POST['department'],
                        school=request.POST['school'],
                        expectedreturndate=expdate,
                        overlappeddate=ovdate)
                    loan.save()
                    avail.available = False
                    avail.save()
                    student.delete()
                    message ="Request is approved"
                    reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
                    return render(request,"libraryhelper/home.html",{'message':message,'reservelist':reservelist,'admin':admin})
                else:
                    message ="No copy availabe at the moment"
                    reservelist = Reservee.objects.filter(datecreated__lte=(datetime.now()-timedelta(days = 3)))
                    return render(request,"libraryhelper/home.html",{'message':message,'reservelist':reservelist,'admin':admin})
    message ="The search input wasn't found in the database"
    reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
    return render(request,"libraryhelper/home.html",{'message':message,'reservelist':reservelist,'admin':admin})


@login_required
def approve(request):
    admin = Liberian.objects.get(user=request.user)
    approvelist = Loan.objects.all().order_by('-dateloaned')
    return render(request,'libraryhelper/approvelist.html',{'admin':admin,'approvelist':approvelist})

#Form created to display reserved student info
@login_required
def approvereserve(request,reserve_pk):
    admin = Liberian.objects.get(user=request.user)
    todo = get_object_or_404(Reservee, pk=reserve_pk)
    form = ReserveForm(instance=todo)
    return render(request, 'libraryhelper/reservresult.html',{'admin':admin,'todo':todo,'form':form})

@login_required
def approvestudent(request,approve_pk):
    admin = Liberian.objects.get(user=request.user)
    if request.method == 'GET':
        todo = get_object_or_404(Loan, pk=approve_pk)
        form = LoanForm(instance=todo)
        return render(request, 'libraryhelper/approvee.html',{'admin':admin,'todo':todo,'form':form})
    elif request.method == 'POST':        
        loan = Loan.objects.get(pk=approve_pk)
        loan.returndate = datetime.now()
        prior = (loan.returndate - loan.dateloaned.replace(tzinfo=None))
        #change hours to days = 7
        if prior > timedelta(hours = 1):
            #to change prior to day use prior.days
            stud = Defaulters.objects.create(copy=loan.copy,surname=request.POST['surname'],firstname=request.POST['firstname'],matric=request.POST['matric'],department=request.POST['department'],school=request.POST['school'],prior=int(prior.seconds//3600))
            stud.save()
            loan.delete()
            message = "Book successfully returned"
            approvelist = Loan.objects.all().order_by('-dateloaned')
            return render(request,'libraryhelper/approvelist.html',{'admin':admin,'approvelist':approvelist,'message':message})

@login_required
def searchapprove(request):
    admin = Liberian.objects.get(user=request.user)
    if request.method == 'GET':
        if request.GET['searchname'] == "":
            message ="You didn't input any name to search for"
            """ Change time to seven days"""
            overduelist = Loan.objects.filter()
            return render(request,"libraryhelper/approvelist.html",{'approvelist':overduelist,'message':message,'admin':admin})
    else: 
        if request.POST['searchby'] == "Firstname":
            overduelist = Loan.objects.filter(firstname__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/approvelist.html",{'approvelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "Surname":
            overduelist = Loan.objects.filter(surname__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/approvelist.html",{'approvelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "School":
            overduelist = Loan.objects.filter(school__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/approvelist.html",{'approvelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "Department":
            overduelist = Loan.objects.filter(department__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/approvelist.html",{'approvelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "matric":
            overduelist = Loan.objects.filter(matric__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/approvelist.html",{'approvelist':overduelist,'admin':admin})
        else:
            message ="The search input wasn't found in the database"
            overduelist = Loan.objects.filter()
            return render(request,"libraryhelper/approvelist.html",{'approvelist':overduelist,'message':message,'admin':admin})

@login_required
def overdue(request):
    admin = Liberian.objects.get(user=request.user)
    #note change hours to days = 7
    elapse = datetime.now()-timedelta(days = 7)
    overduelist = Loan.objects.filter(dateloaned__lt= elapse)
    return render(request,"libraryhelper/overdue.html",{'admin':admin,'overduelist':overduelist})

@login_required
def searchoverdue(request):
    admin = Liberian.objects.get(user=request.user)
    if request.method == 'GET':
        if request.GET['searchname'] == "":
            message ="You didn't input any name to search for"
            """ Change time to seven days"""
            overduelist = Loan.objects.filter(dateloaned__lt=(datetime.now()-timedelta(hours = 1)))
            return render(request,"libraryhelper/overdue.html",{'admin':admin,'overduelist':overduelist,'message':message})
    else: 
        if request.POST['searchby'] == "Firstname":
            overduelist = Loan.objects.filter(firstname__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/overdue.html",{'overduelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "Surname":
            overduelist = Loan.objects.filter(surname__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/overdue.html",{'overduelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "School":
            overduelist = Loan.objects.filter(school__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/overdue.html",{'overduelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "Department":
            overduelist = Loan.objects.filter(department__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/overdue.html",{'overduelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "matric":
            overduelist = Loan.objects.filter(matric__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/overdue.html",{'overduelist':overduelist,'admin':admin})
        else:
            message ="The search input wasn't found in the database"
            overduelist = Loan.objects.filter()
            return render(request,"libraryhelper/overdue.html",{'overduelist':overduelist,'message':message,'admin':admin})
            
@login_required
def defaulters(request):
    admin = Liberian.objects.get(user=request.user)
    overduelist = Defaulters.objects.all()
    return render(request,"libraryhelper/defaulters.html",{'admin':admin,'overduelist':overduelist})

@login_required
def searchdefault(request):
    admin = Liberian.objects.get(user=request.user)
    if request.method == 'GET':
        if request.GET['searchname'] == "":
            message ="You didn't input any name to search for"
            overduelist = Defaulters.objects.all()
            return render(request,"libraryhelper/defaulters.html",{'overduelist':overduelist,'message':message,"admin":admin})
    else: 
        if request.POST['searchby'] == "Firstname":
            overduelist = Defaulters.objects.filter(firstname__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/defaulters.html",{'overduelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "Surname":
            overduelist = Defaulters.objects.filter(surname__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/defaulters.htmll",{'overduelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "School":
            overduelist = Defaulters.objects.filter(school__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/defaulters.html",{'overduelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "Department":
            overduelist = Defaulters.objects.filter(department__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/defaulters.html",{'overduelist':overduelist,'admin':admin})
        elif request.POST['searchby'] == "matric":
            overduelist = Defaulters.objects.filter(matric__icontains=request.POST['searchname'])
            return render(request,"libraryhelper/defaulters.html",{'overduelist':overduelist,'admin':admin})
        else:
            message ="The search input wasn't found in the database"
            overduelist = Defaulters.objects.filter()
            return render(request,"libraryhelper/defaulters.html",{'overduelist':overduelist,'message':message,'admin':admin})
    
@login_required
def viewdefaulters(request,defaulter_pk):
    admin = Liberian.objects.get(user=request.user)
    if request.method == "GET":
        todo = get_object_or_404(Defaulters, pk=defaulter_pk)
        form = DefaulterForm(instance=todo)
        return render(request, 'libraryhelper/defaulterresult.html',{'admin':admin,'todo':todo,'form':form}) 
    elif request.method == "POST":
        defaulter = Defaulters.objects.get(pk=defaulter_pk)
        defaulter.delete()
        reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
        return render(request,'libraryhelper/home.html',{'admin':admin,'reservelist':reservelist})

@login_required
def addbook(request):
    admin = Liberian.objects.get(user=request.user)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.errors:
            form = BookForm()
            message = "Error discovered in form input please go throught it"
            return render(request, 'libraryhelper/addbook.html', {'admin':admin,'form': form,'message':message})
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days=7)))
            return render(request, 'libraryhelper/home.html', {'admin':admin,'reservelist': reservelist})
    else:
        form = BookForm()
    return render(request, 'libraryhelper/addbook.html', {'admin':admin,'form': form})



@login_required
def addcopy(request):
    admin = Liberian.objects.get(user=request.user)
    if request.method == "GET":
        form = CopyForm()
        return render(request, 'libraryhelper/addcopy.html', {'admin':admin,'form': form})
    elif request.method == "POST":
        try:
            book = Book.objects.get(id=request.POST['book'])
            copy = Copy.objects.create(
                book=book,
                copyname=request.POST['copyname'],
                available=request.POST['available']
            )
            reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days=3)))
            return render(request, 'libraryhelper/home.html', {'admin':admin,'reservelist': reservelist})
        except (IntegrityError, Book.DoesNotExist):
            # If there is an IntegrityError or the book does not exist, return to the form with an error message
            form = CopyForm(request.POST)
            form.add_error('book', 'Please select a valid book.')
            return render(request, 'libraryhelper/addcopy.html', {'admin':admin,'form': form})

@login_required
def approvecopylist(request):
    if request.method == "GET":
        unapplist = Copy.objects.filter(approve=False)
        return render(request, 'libraryhelper/approvecopylist.html',{'unapplist':unapplist})

@login_required
def approvebooklist(request):
    if request.method == "GET":
        unapplist = Book.objects.filter(approve=False)
        return render(request, 'libraryhelper/approvebooklist.html',{'unapplist':unapplist})

@login_required
def approvecopy(request,copy_pk):
    booki = get_object_or_404(Copy, pk=copy_pk)
    if request.method == "GET":
        form = CopyForm(instance=booki)
        return render(request, 'libraryhelper/approvecopy.html',{'form':form})
    elif request.method == "POST":
        try:
            form = CopyForm(request.POST, instance=booki)
            booki.approve = True
            form.save()
            return redirect('approvecopylist')
        except ValueError:
                return render(request,'libraryhelper/approvecopy.html',{'form':CopyForm(),'error':'Is bad data passed in'}) 

@login_required
def approvebook(request,copy_pk):
    booki = get_object_or_404(Book, pk=copy_pk)
    if request.method == "GET":
        form = BookForm(instance=booki)
        return render(request, 'libraryhelper/approvebook.html',{'form':form})
    elif request.method == "POST":
        try:
            form = BookForm(request.POST, instance=booki)
            booki.approve = True
            form.save()
            return redirect('approvebooklist')
        except ValueError:
                return render(request,'libraryhelper/approvebook.html',{'form':BookForm(),'error':'Is bad data passed in'}) 


""""    CODE TO RETURN BACK TO LIBERIAN HOMEPAGE
        reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
        return render(request,'libraryhelper/home.html',{'reservelist':reservelist})
"""
@login_required
def addliberian(request):
    if request.method == "GET":
        return render(request,'libraryhelper/addliberian.html')
    else:
        if request.POST['passwordone'] == request.POST['passwordtwo']:
            try:
                user = User.objects.create_user(request.POST['username'],password = request.POST['passwordone'],first_name=request.POST['firstname'],last_name=request.POST['surname'],email=request.POST['email'],)
                user.save()
                return redirect('personalinfo')
            except IntegrityError:
                return render(request,'libraryhelper/addliberian.html',{'error':'The username is taken choose another one'})                
        else:
            return render(request,'libraryhelper/addliberian.html',{'error':'password dosen\'t match'})

@login_required
def personalinfo(request):
    if request.method == "GET":
        form = LiberianForm
        return render(request, 'libraryhelper/libpersonalinfo.html',{'form':form})
    elif request.method == "POST":
        lib = LiberianForm(request.POST)
        lib.save()
        return redirect(liberianlist)

@login_required
def liberianlist(request):
    for i in Liberian.objects.all():
        if i.user.last_login:
            lastlog = i.user.last_login
            treshold = datetime.combine(datetime.today(), time(7, 30, tzinfo=timezone.get_current_timezone()))
            if lastlog and lastlog > treshold:
                if i.last_log < treshold:
                    i.last_log = lastlog
                    i.save()
            """ The code in the comment is to show that i.save() is working and the 
            if condition is working"""
            # else:
            #     print("++++++++++++++++++++")
            #     i.last_log = datetime.now()
            #     i.save()
    alllib = Liberian.objects.all()
    return render(request, 'libraryhelper/alllib.html', {'alllib':alllib})

@login_required
def liberianinfo(request,copy_pk):
    lib = get_object_or_404(Liberian, id=copy_pk)
    if request.method == 'GET':
        form = LiberianForm(instance=lib)
        return render(request, 'libraryhelper/personalinfo.html',{'form':form})
    else:
        try:
            form = LiberianForm(request.POST, instance=lib)
            form.save()
            return redirect('liberianlist')
        except ValueError:
                return render(request,'libraryhelper/personalinfo.html',{'form':LiberianForm(),'error':'Is bad data passed in'}) 

@login_required
def makeadmin(request):
    lib = get_object_or_404(Liberian,user=request.user)
    if request.method == 'POST':
        lib.isAdmin = True
        lib.save()
        return redirect('liberianlist')

@login_required
def deleteliberian(request):
    lib = get_object_or_404(Liberian,user=request.user)
    if request.method == 'POST':
        lib.delete()
        return redirect('liberianlist')


def logoutuser(request):
    logout(request)
    return render(request,'libraryhelper/index.html')

