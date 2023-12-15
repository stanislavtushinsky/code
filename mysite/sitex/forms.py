from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterForm(forms.ModelForm):

    email = forms.CharField(label='email', widget=forms.EmailInput(attrs={
        'placeholder':'Email',
        'class':'regform'
    }))
    nickname = forms.CharField(label='nickname', widget=forms.TextInput(attrs={
        'placeholder':'Nickname',
        'class':'regform'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
        'class':'regform'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'regform'
    }))

    class Meta:
        model = User
        fields = ('nickname', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active = False
        if commit:
            user.save()
        return user
    



class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'placeholder':'Email',
        'class':'logform'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
        'class':'logform'
    }))
    

class ConvertForm(forms.Form):
    Options = (
        ('EUR', 'EUR'),
        ('RUB', 'RUB'),
        ('USD', 'USD'),
        ('BYN', 'BYN'),
    )
    fcurrency = forms.ChoiceField(label='Form', widget=forms.Select, choices=Options)
    scurrency = forms.ChoiceField(label='To', widget=forms.Select, choices=Options)
    amount = forms.IntegerField(label='Amount')