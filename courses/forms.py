from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Coupon, Article, PDFDocument

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CouponForm(forms.Form):
    code = forms.CharField(max_length=20)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not Coupon.objects.filter(code=code, is_active=True).exists():
            raise forms.ValidationError("This coupon is invalid or expired.")
        return code

class CouponForm(forms.Form):
    code = forms.CharField(max_length=50, label="Coupon Code")


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_premium']

class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['title', 'pdf_file', 'is_premium']
