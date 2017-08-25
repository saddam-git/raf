from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth import get_user_model
from .utils import ActivationMailFormMixin
from django.core.exceptions import ValidationError
import logging
from .models import Profile
from django.utils.text import slugify


logger = logging.getLogger(__name__)




class ResendActivationEmailForm(ActivationMailFormMixin,forms.Form):
    email = forms.EmailField()

    mail_validation_error = ('Could not re send activation email please try again later (sorry)')

    def save(self,**kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except:
            logger.warning ('Resend Activation Email: no user with email: {}'.format(self.cleaned_data['email']))
            return None
        self.send_mail(user=user,**kwargs)
        return user





class UserCreationForm(ActivationMailFormMixin,BaseUserCreationForm):
    name = forms.CharField(max_length=255)
    mail_validation_error = (
        'User created could not sent activation email Please try again later (Sorry!!)'
    )
    class Meta:
        model = get_user_model()
        fields = ['name','email']


    def clean_username(self):
        name = self.cleaned_data['name']
        disallowed = (
            'activate',
            'create',
            'disabel',
            'login',
            'logout',
            'password',
            'profile',
        )
        if name is disallowed:
            raise ValidationError ("A user with that username already exist")
        return name



    def save(self, **kwargs):
        user = super().save(commit=False)
        if not user.pk:
            user.is_active = False
            send_mail = True

        else :
            send_mail = False

        user.save()
        self.save_m2m()
        Profile.objects.update_or_create(user = user,defaults={'name':self.cleaned_data['name'],
                                                               'slug':slugify(self.cleaned_data['name'])})

        if send_mail:
            self.send_mail(user= user, **kwargs)
        return user



