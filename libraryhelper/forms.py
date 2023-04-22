from django.forms import ModelForm
from .models import Book, Copy,Reservee,Loan,Defaulters,Liberian



# STYLING DJANGO FORMS
class ReserveForm(ModelForm):
    class Meta:
        model = Reservee
        fields = ['firstname', 'surname', 'department','school','matric','book']


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = ['firstname', 'surname', 'department','school','matric','copy']


class DefaulterForm(ModelForm):
    class Meta:
        model = Defaulters
        fields = ['firstname', 'surname', 'department','school','matric','copy','prior']


class BookForm(ModelForm):
    class Meta:
        model = Book
        #note I will check if user.admin here
        fields = ['booktitle','bookimg','authors','edition','booktype','deptclass','year','isbn','aisle','description',"pdf_available",'pdf_file']

class CopyForm(ModelForm):
    class Meta:
        model = Copy
        fields = ['book','copyname','available']


class LiberianForm(ModelForm):
    class Meta:
        model = Liberian
        fields = ['user','dob','address','bio','gender','nin','profileimg','isAdmin']

    

#EG:
"""
class UserInfoForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                })
        }

"""

