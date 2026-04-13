from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请设置密码'}))
    password2 = forms.CharField(label='确认密码',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'department']
        labels = {'username': '用户名', 'first_name': '姓名', 'department': '部门/班级'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入真实姓名'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入部门/班级'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError('两次密码不一致')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'student'
        if commit:
            user.save()
        return user
