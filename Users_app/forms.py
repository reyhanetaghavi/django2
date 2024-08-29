from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Profile

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("این شماره تلفن قبلاً ثبت نام شده است.")
        return phone_number

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("پسووردها باید برابر باشند.")
        
        if len(password1) < 8:
            raise forms.ValidationError("پسوورد باید حداقل 8 کاراکتر باشد.")
        
        # شما می‌توانید شرایط بیشتری اضافه کنید مثل چک کردن اینکه پسوورد معمول نباشد

        return password2



class ProfileForm(forms.ModelForm):
    GENDER = [
        ('خانم','خانم'), ('آقا','آقا')
    ]

    name = forms.CharField(max_length=30, required=True, label="نام")
    family_name = forms.CharField(max_length=30, required=True, label="نام خانوادگی")
    gender = forms.ChoiceField(choices=GENDER, required=True, label="جنسیت")

    class Meta:
        model = Profile
        fields = ['name', 'family_name','gender']




class LoginForm(forms.Form):
    username_or_phone = forms.CharField(max_length=15, required=True, label="نام کاربری یا شماره تلفن")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="رمز عبور")

