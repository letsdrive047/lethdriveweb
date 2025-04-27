from django import forms

class EmployeeRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    ROLE_CHOICES = [
        ('driver', 'Driver'),
        ('admin', 'admin'),
        ('patner', 'patner'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select())

    profile_pic = forms.ImageField(label="Profile Picture")
    dl = forms.ImageField(label="Driving License ")
    



def clean_profile_pic(self):
    profile_pic = self.cleaned_data.get("profile_pic")
    if profile_pic:
        if not profile_pic.content_type.startswith('image'):
            raise forms.ValidationError("Only image files (JPG, PNG) are allowed for the profile picture.")
    return profile_pic

def clean_dl(self):
    dl = self.cleaned_data.get("dl")
    if dl:
        if not dl.content_type.startswith('image'):
            raise forms.ValidationError("Only image files (JPG, PNG) are allowed for the driving license.")
    return dl