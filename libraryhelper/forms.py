from django.forms import ModelForm
from django import forms
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


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        dept = [ 
                    ('AEC','AGRIC EXTENSION & COMMUNICATION TECHNOLOGY'),
                    ('AGE','AGRICULTURAL ENGINEERING'),
                    ('ARE','AGRICULTURE RESOURCE ECONOMICS'),
                    ('APH','ANIMAL PRODUCTION & HEALTH SERVICES'),
                    ('AGY','APPLIED GEOLOGY'),
                    ('AGP','APPLIED GEOPHYSICS'),
                    ('ARC','ARCHITECTURE'),
                    ('BCH','BIOCHEMISTRY'),
                    ('BIO','BIOLOGY'),
                    ('BMT','BIOMEDICAL TECHNOLOGY'),
                    ('BTH','BIOTECHNOLOGY'),
                    ('BLD','BUILDING'),
                    ('CVE','CIVIL ENGINEERING'),
                    ('CPE','COMPUTER ENGINEERING'),
                    ('CSC','COMPUTER SCIENCE'),
                    ('CSP','CROP SOIL & PEST MANAGEMENT'),
                    ('CYS','CYBER SECURITY'),
                    ('ECM','ECOTOURISM & WILDLIFE MANAGEMENT'),
                    ('EEE','ELECTRICAL ELECTRONICS ENGINEERING'),
                    ('ESM','ESTATE MANAGEMENT'),
                    ('FAT','FISHERIES & AQUACULTURE'),
                    ('FST','FOOD SCIENCE & TECHNOLOGY'),
                    ('FWT','FORESTRY & WOOD TECHNOLOGY'),
                    ('HUA','HUMAN ANATOMY'),
                    ('IPE','INDUSTRIAL & PRODUCTION ENGINEERING'),
                    ('CHE','INDUSTRIAL CHEMISTRY'),
                    ('IDD','INDUSTRIAL DESIGN'),
                    ('IMT','INDUSTRIAL MATHEMATICS'),
                    ('ICT','INFORMATION & COMMUNICATION TECHNOLOGY'),
                    ('IFS','INFORMATION SYSTEMS'),
                    ('IFT','INFORMATION TECHNOLOGY'),
                    ('MST','MARINE SCIENCE & TECHNOLOGY'),
                    ('MTS','MATHEMATICS'),
                    ('MEE','MECHANICAL ENGINEERING'),
                    ('MME','METALLURGICAL & MATERIALS ENGINEERING'),
                    ('MTL','METEOROLOGY'),
                    ('MCB','MICROBIOLOGY'),
                    ('MNE','MINING ENGINEERING'),
                    ('PHY','PHYSICS'),
                    ('PSY','PHYSIOLOGY'),
                    ('QSV','QUANTITY SURVEYING'),
                    ('RSG','REMOTE SENSING & GEOSCIENCES INFORMATION SYSTEM'),
                    ('SFE','SOFTWARE ENGINEERING'),
                    ('STA','STATISTICS'),
                    ('SVG','SURVEYING & GEOINFORMATICS'),
                    ('URP','URBAN & REGIONAL PLAN')
        ]
        booktype =[
            ('book','Book'),
            ('journal','Journal'),
            ('research','Research')
        ]
        fields = ['booktitle','authors','edition','booktype','deptclass','year','isbn','aisle','description',"pdf_available"]
        widgets = {
            'booktitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'authors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter authors'}),
            'edition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter edition'}),
            'booktype': forms.Select(choices=booktype,attrs={'class': 'form-control'}),
            'deptclass': forms.Select(choices=dept,attrs={'class': 'form-control'}),
            'year': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter year'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ISBN'}),
            'aisle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter aisle'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
            'pdf_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CopyForm(ModelForm):
    class Meta:
        model = Copy
        fields = ['book','copyname','available']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'copyname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter copy name'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


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

