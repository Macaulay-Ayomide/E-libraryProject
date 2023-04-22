from curses import longname
from django.shortcuts import redirect, render, get_object_or_404
from .models import Book, Copy, Liberian, Reservee, Loan, Review, Defaulters
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, tzinfo
from .forms import BookForm, ReserveForm,LoanForm,DefaulterForm,CopyForm,LiberianForm
from django.contrib.auth.models import User
from django.db import IntegrityError


# Create your views here.
###USERS METHOD
def index(request):
    book = Book.objects.all().order_by('-dateadded')
    return render(request,"libraryhelper/index.html",{'book':book})

def bookcatalouge(request,varone,vartwo):
    if vartwo != "None":
        items = Book.objects.filter(booktitle__startswith=varone,deptclass=vartwo).order_by('booktitle') 
        return render(request, 'libraryhelper/bookcatalog.html', {'items': items,'varone':varone,'vartwo':vartwo})
    else:
        items = Book.objects.filter(booktitle__startswith=varone).order_by('booktitle') 
        return render(request, 'libraryhelper/bookcatalog.html', {'items': items,'varone':varone,'vartwo':vartwo})

def booksearch(request):
    return render(request,"libraryhelper/booksearch.html")


def bookdetail(request,book_pk):
    bookdetail = get_object_or_404(Book, pk=book_pk)
    return render(request,"libraryhelper/bookdetail.html",{'book':bookdetail})

def bookreservelist(request, book_pk):
    reservelist = Reservee.objects.filter(book=book_pk)
    return render(request,"libraryhelper/reservelist.html",{'reservelist':reservelist})


def bookreserve(request, book_pk):
    if request.method == 'GET':
        copy = Copy.objects.filter(book=book_pk,available=True)
        return render(request,"libraryhelper/bookreserve.html",{'copy':copy})
    elif request.method == 'POST':
        #check for blank
        if (request.POST['Firstname'] == "") | (request.POST['Surname'] == "") | (request.POST['Matric'] == ""):
            error = "You didn't fill in your first name"
            return render(request,"libraryhelper/bookreserve.html",{'error':error})
        #Create an object for reserve
        book=Book.objects.get(pk=book_pk)
        reservee = Reservee.objects.create(book=book,surname=request.POST['Surname'],firstname=request.POST['Firstname'],matric=request.POST['Matric'],department=request.POST['Department'],school=request.POST['School'])
        print(reservee.id)
        reservee.save()
        return redirect('bookreservelist',book_pk=book_pk)
    return render(request,"libraryhelper/bookdetail.html",{'book':bookdetail})



def searchresult(request):
    #Book search made withouth specifying if its by authors name or book title
    if request.GET['bookname'] == "":
        message ="You didn't input any name to search for"
        return render(request,"libraryhelper/booksearch.html",{'message':message})
    else:
        if request.GET['searchby'] == "None" and request.GET['department'] == "None" and request.GET['booktype'] == "None":
            booklistone = Book.objects.filter(booktitle__icontains=request.GET['bookname'])
            booklisttwo = Book.objects.filter(authors__icontains=request.GET['bookname'])
            booklist = booklistone | booklisttwo
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        elif request.GET['searchby'] == "None" and request.GET['department'] != "None" and request.GET['booktype'] == "None":
            booklistone = Book.objects.filter(booktitle__icontains=request.GET['bookname'],deptclass=request.GET['department'])
            booklisttwo = Book.objects.filter(authors__icontains=request.GET['bookname'],deptclass=request.GET['department'])
            booklist = booklistone | booklisttwo
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        elif request.GET['searchby'] == "None" and request.GET['department'] == "None" and request.GET['booktype'] != "None":
            print(request.GET['booktype'])
            booklistone = Book.objects.filter(booktitle__icontains=request.GET['bookname'],booktype=request.GET['booktype'])
            booklisttwo = Book.objects.filter(authors__icontains=request.GET['bookname'],booktype=request.GET['booktype'])
            booklist = booklistone | booklisttwo
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        elif request.GET['searchby'] == "None" and request.GET['department'] != "None" and request.GET['booktype'] != "None":
            booklistone = Book.objects.filter(booktitle__icontains=request.GET['bookname'],deptclass=request.GET['department'],booktype=request.GET['booktype'])
            booklisttwo = Book.objects.filter(authors__icontains=request.GET['bookname'],deptclass=request.GET['department'],booktype=request.GET['booktype'])
            booklist = booklistone | booklisttwo
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        #For book authors
        #
        elif request.GET['department'] == "None" and request.GET['booktype'] == "None":         
            booklist = Book.objects.filter(authors__icontains=request.GET['bookname'])
            print(booklist)
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        elif request.GET['department'] != "None" and request.GET['booktype'] == "None":
            booklist = Book.objects.filter(authors__icontains=request.GET['bookname'],deptclass=request.GET['department'])
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        elif request.GET['department'] == "None" and request.GET['booktype'] != "None":
            booklist = Book.objects.filter(authors__icontains=request.GET['bookname'],booktype=request.GET['booktype'])
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        elif request.GET['department'] != "None" and request.GET['booktype'] != "None":
            booklist = Book.objects.filter(authors__icontains=request.GET['bookname'],deptclass=request.GET['department'],booktype=request.GET['booktype'])
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        #For book titles
        #
        elif request.GET['searchby'] == "Book Title" and request.GET['department'] == "None" and request.GET['booktype'] == "None":
            booklist = Book.objects.filter(booktitle__icontains=request.GET['bookname'])
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        elif request.GET['searchby']== "Book Title" and request.GET['department'] != "None" and request.GET['booktype'] == "None":
            booklist = Book.objects.filter(booktitle__icontains=request.GET['bookname'],deptclass=request.GET['department'])
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        elif request.GET['searchby'] == "Book Title" and request.GET['department'] == "None" and request.GET['booktype'] != "None":
            booklist = Book.objects.filter(booktitle__icontains=request.GET['bookname'],booktype=request.GET['booktype'])
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        elif request.GET['searchby'] == "Book Title" and request.GET['department'] == "None" and request.GET['booktype'] == "None":
            booklist = Book.objects.filter(booktitle__icontains=request.GET['bookname'],deptclass=request.GET['department'],booktype=request.GET['booktype'])
            return render(request,"libraryhelper/booksearchresult.html",{'booklist':booklist})
        message ="The application is unable to ubderstand your query"
    return render(request,"libraryhelper/booksearch.html",{'message':message})


###Liberian methods
def loginuser(request):
    if request.method == 'GET':
        return render(request,'libraryhelper/login.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password =request.POST['password'])
        if user is None:
            return render(request,'todo/login.html',{'form':AuthenticationForm(),'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')


#@login_required
def home(request):
    reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
    return render(request,'libraryhelper/home.html',{'reservelist':reservelist})

def searchreservation(request):
    if request.method == 'GET':
        if request.GET['searchname'] == "":
            message ="You didn't input any name to search for"
            reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
            return render(request,"libraryhelper/home.html",{'message':message,'reservelist':reservelist})
        else: 
            if request.GET['searchby'] == "Firstname":
                result = Reservee.objects.get(firstname=request.GET['searchname'])
            elif request.GET['searchby'] == "Surname":
                result = Reservee.objects.get(surname=request.GET['searchname'])
            elif request.GET['searchby'] == "School":
                result = Reservee.objects.get(schoole=request.GET['searchname'])
            elif request.GET['searchby'] == "Department":
                result = Reservee.objects.get(department=request.GET['searchname'])
            elif request.GET['searchby'] == "matric":
                result = Reservee.objects.get(matric=request.GET['searchname'])
            if result:
                todo = get_object_or_404(Reservee, pk=result.pk)
                form = ReserveForm(instance=todo)
                return render(request, 'libraryhelper/reservresult.html',{'todo':todo,'form':form})
    elif request.method == 'POST':
        if Loan.objects.filter(matric=request.POST['matric']).count() > 3:
            message ="The student can't have more then three books"
            return render(request,"libraryhelper/reservresult.html",{'message':message})
        checker = Review.objects.filter(matric=request.POST['matric']).first()
        if checker:
            if (checker.totalretbook /checker.totalloanbook) < 0.335 and  ((datetime.now()- checker.lstreturndate) < 30) :
                message ="The student can't have a very low return rate"
            return render(request,"libraryhelper/reservresult.html",{'message':message})
        student = Reservee.objects.get(matric=request.POST['matric'])
        avail = Copy.objects.filter(book=student.book,available=True).first()
        if avail:
            print("Sader")
            loan = Loan.objects.create(copy=avail,surname=request.POST['surname'],firstname=request.POST['firstname'],matric=request.POST['matric'],department=request.POST['department'],school=request.POST['school'])
            loan.save()
            avail.available = False
            avail.save()
            student.delete()
            message ="Request is approved"
            reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
            return render(request,"libraryhelper/home.html",{'message':message,'reservelist':reservelist})

        else:
            print("Sadem")
            message ="No copy availabe at the moment"
            reservelist = Reservee.objects.filter(datecreated__lte=(datetime.now()-timedelta(days = 3)))
            return render(request,"libraryhelper/home.html",{'message':message,'reservelist':reservelist})
    print("Shade")
    message ="The search input wasn't found in the database"
    reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
    return render(request,"libraryhelper/home.html",{'message':message,'reservelist':reservelist})



def approve(request):
    approvelist = Loan.objects.all().order_by('-dateloaned')
    return render(request,'libraryhelper/approvelist.html',{'approvelist':approvelist})

#Form created to display reserved student info
def approvereserve(request,reserve_pk):
    todo = get_object_or_404(Reservee, pk=reserve_pk)
    form = ReserveForm(instance=todo)
    return render(request, 'libraryhelper/reservresult.html',{'todo':todo,'form':form})


def approvestudent(request,approve_pk):
    if request.method == 'GET':
        todo = get_object_or_404(Loan, pk=approve_pk)
        form = LoanForm(instance=todo)
        return render(request, 'libraryhelper/approvee.html',{'todo':todo,'form':form})
    elif request.method == 'POST':        
        loan = Loan.objects.get(pk=approve_pk)
        loan.returndate = datetime.now()
        print(type(loan.returndate))
        print(type(loan.dateloaned))
        prior = (loan.returndate - loan.dateloaned.replace(tzinfo=None))
        #change hours to days = 7
        if prior > timedelta(hours = 1):
            #to change prior to day use prior.days
            stud = Defaulters.objects.create(copy=loan.copy,surname=request.POST['surname'],firstname=request.POST['firstname'],matric=request.POST['matric'],department=request.POST['department'],school=request.POST['school'],prior=int(prior.seconds//3600))
            stud.save()
            loan.delete()
            message = "Book successfully returned"
            approvelist = Loan.objects.all().order_by('-dateloaned')
            return render(request,'libraryhelper/approvelist.html',{'approvelist':approvelist,'message':message})


def overdue(request):
    #note change hours to days = 7
    overduelist = Loan.objects.filter(dateloaned__lt=(datetime.now()-timedelta(hours = 1)))
    return render(request,"libraryhelper/overdue.html",{'overduelist':overduelist})


def searchoverdue(request):
    if request.method == 'GET':
        if request.GET['searchname'] == "":
            message ="You didn't input any name to search for"
            overduelist = Loan.objects.filter(dateloaned__lt=(datetime.now()-timedelta(hours = 1)))
            return render(request,"libraryhelper/overdue.html",{'overduelist':overduelist,'message':message})
        else: 
            if request.GET['searchby'] == "Firstname":
                result = Loan.objects.get(firstname=request.GET['searchname'])
            elif request.GET['searchby'] == "Surname":
                result = Loan.objects.get(surname=request.GET['searchname'])
            elif request.GET['searchby'] == "School":
                result = Loan.objects.get(schoole=request.GET['searchname'])
            elif request.GET['searchby'] == "Department":
                result = Loan.objects.get(department=request.GET['searchname'])
            elif request.GET['searchby'] == "matric":
                result = Loan.objects.get(matric=request.GET['searchname'])
            if result:
                todo = get_object_or_404(Loan, pk=result.pk)
                form = LoanForm(instance=todo)
                return render(request, 'libraryhelper/overdueresult.html',{'todo':todo,'form':form})


def defaulters(request):
    overduelist = Defaulters.objects.all()
    return render(request,"libraryhelper/defaulters.html",{'overduelist':overduelist})

def searchdefault(request):
    if request.method == 'GET':
        if request.GET['searchname'] == "":
            message ="You didn't input any name to search for"
            overduelist = Defaulters.objects.all()
            return render(request,"libraryhelper/defaulters.html",{'overduelist':overduelist,'message':message})
        else: 
            if request.GET['searchby'] == "Firstname":
                result = Defaulters.objects.get(firstname=request.GET['searchname'])
            elif request.GET['searchby'] == "Surname":
                result = Defaulters.objects.get(surname=request.GET['searchname'])
            elif request.GET['searchby'] == "School":
                result = Defaulters.objects.get(schoole=request.GET['searchname'])
            elif request.GET['searchby'] == "Department":
                result = Defaulters.objects.get(department=request.GET['searchname'])
            elif request.GET['searchby'] == "matric":
                result = Defaulters.objects.get(matric=request.GET['searchname'])
            if result:
                todo = get_object_or_404(Defaulters, pk=result.pk)
                form = DefaulterForm(instance=todo)
                return render(request, 'libraryhelper/defaulterresult.html',{'todo':todo,'form':form})


def viewdefaulters(request,defaulter_pk):
    if request.method == "GET":
        todo = get_object_or_404(Defaulters, pk=defaulter_pk)
        form = DefaulterForm(instance=todo)
        return render(request, 'libraryhelper/defaulterresult.html',{'todo':todo,'form':form}) 
    elif request.method == "POST":
        defaulter = Defaulters.objects.get(pk=defaulter_pk)
        defaulters.delete()
        reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
        return render(request,'libraryhelper/home.html',{'reservelist':reservelist})


def addbook(request):
    if request.method == "GET":
        form = BookForm
        return render(request, 'libraryhelper/addbook.html',{'form':form})
    else:
        book = Book.objects.create(booktitle=request.POST['booktitle'],authors=request.POST['authors'],edition=request.POST['edition'],booktype=request.POST['booktype'],deptclass=request.POST['deptclass'],year=request.POST['year'],isbn=request.POST['isbn'],aisle=request.POST['aisle'],description=request.POST['description'],pdf_available=request.POST['pdf_available'],pdf_file=request.POST['pdf_file'])
        book.save()
        reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
        return render(request,'libraryhelper/home.html',{'reservelist':reservelist})

def addcopy(request):
    if request.method == "GET":
        form = CopyForm
        return render(request, 'libraryhelper/addcopy.html',{'form':form})
    else:
        book = Book.objects.get(id=request.POST['book'])
        try:
            copy = Copy.objects.create(book=book,copyname=request.POST['copyname'],available=request.POST['available'])
            copy.save()
            reservelist = Reservee.objects.filter(datecreated__gte=(datetime.now()-timedelta(days = 3)))
            return render(request,'libraryhelper/home.html',{'reservelist':reservelist})
        except IntegrityError:
            lastindex = Copy.objects.filter().order_by('-id')[0]
            form = CopyForm
            return render(request, 'libraryhelper/addcopy.html',{'lastindex':lastindex,'form':form})


def approvecopylist(request):
    if request.method == "GET":
        unapplist = Copy.objects.filter(approve=False)
        return render(request, 'libraryhelper/approvecopylist.html',{'unapplist':unapplist})


def approvebooklist(request):
    if request.method == "GET":
        unapplist = Book.objects.filter(approve=False)
        return render(request, 'libraryhelper/approvebooklist.html',{'unapplist':unapplist})


def approvecopy(request,copy_pk):
    booki = get_object_or_404(Copy, pk=copy_pk)
    if request.method == "GET":
        form = CopyForm(instance=booki)
        return render(request, 'libraryhelper/approvebook.html',{'form':form})
    elif request.method == "POST":
        try:
            form = CopyForm(request.POST, instance=booki)
            booki.approve = True
            form.save()
            return redirect('approvecopylist')
        except ValueError:
                return render(request,'libraryhelper/approvecopy.html',{'form':CopyForm(),'error':'Is bad data passed in'}) 




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


def personalinfo(request):
    if request.method == "GET":
        form = LiberianForm
        return render(request, 'libraryhelper/libpersonalinfo.html',{'form':form})
    elif request.method == "POST":
        lib = LiberianForm(request.POST)
        lib.save()
        return redirect(liberianlist)


def liberianlist(request):
    alllib = Liberian.objects.all()
    return render(request, 'libraryhelper/alllib.html',{'alllib':alllib})


def liberianinfo(request,user_pk):
    lib = get_object_or_404(Liberian, user=request.user)
    if request.method == 'GET':
        form = LiberianForm(instance=lib)
        return render(request, 'todo/viewtodo.html',{'lib':lib,'form':form})
    else:
        try:
            form = LiberianForm(request.POST, instance=lib)
            form.save()
            return redirect('liberianlist')
        except ValueError:
                return render(request,'todo/createtodo.html',{'form':LiberianForm(),'error':'Is bad data passed in'}) 


def makeadmin(request):
    lib = get_object_or_404(Liberian,user=request.user)
    if request.method == 'POST':
        lib.isAdmin = True
        lib.save()
        return redirect('liberianlist')


def deleteliberian(request):
    lib = get_object_or_404(Liberian,user=request.user)
    if request.method == 'POST':
        lib.delete()
        return redirect('liberianlist')




