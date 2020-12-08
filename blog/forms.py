# blog/forms.py

from django.forms import ModelForm, TextInput, Textarea

from blog.models import Comment  #, Reply

from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.http import HttpResponse



class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'コメント内容',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }


#class ReplyForm(ModelForm):
#    class Meta:
#        model = Reply
#        fields = ('author', 'text')
#        widgets = {
#            'author': TextInput(attrs={
#                'class': 'form-control',
#                'placeholder': '名前',
#            }),
#            'text': Textarea(attrs={
#                'class': 'form-control',
#                'placeholder': '返信内容',
#            }),
#        }
#        labels = {
#            'author': '',
#            'text': '',
#        }



class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    def send_email(self):
        subject = "お問い合わせ"
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = '送信者名: {0}\nメールアドレス {1}\nメッセージ {2}'.format(name, email, message)
        try:
            from_email = 'gattinobianco22@gmail.com'
            to_list = [
                'gattinobianco22@gmail.com'
            ]
            cc_list = [
                email
            ]
            message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
            message.send()
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")
