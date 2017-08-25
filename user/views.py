from django.shortcuts import render
from django.contrib.auth import get_user, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.template.response import TemplateResponse
from raf import settings

################## Signup ####################
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse_lazy
from .forms import UserCreationForm
from .utils import MailContextViewMixin,ProfilGetObjectMixin
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.messages import error
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.messages import success
from django.views.decorators.cache import never_cache
from .forms import ResendActivationEmailForm
from .models import Profile
from django.views.generic import DeleteView,View,DetailView,UpdateView


class DisableAccount(View):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = 'user/user_confirm_delete.html'

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(request, self.template_name)

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def post(self, request):
        user = get_user(request)
        user.set_unusable_password()
        user.is_active = False
        user.save()
        logout(request)
        return redirect(self.success_url)


class Signup(View):
    form_class = UserCreationForm
    success_url = reverse_lazy('tag_list_view')
    template_name = 'user/signup.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        bound_form = UserCreationForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            username = bound_form.cleaned_data.get('username')
            raw_password = bound_form.cleaned_data.get('password1')
            email = bound_form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password, email=email)
            login(request, user)
            return redirect(self.success_url)



        return render(request, self.template_name, {'form': bound_form})


class CreateAccount(MailContextViewMixin, View):
    form_class = UserCreationForm
    success_url = reverse_lazy('dj-auth:create_done')
    template_name = 'user/user_create.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(request, self.template_name, {'form': self.form_class()})

    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            bound_form.save(**self.get_save_kwargs(request))
            if bound_form.mail_sent:
                return redirect(self.success_url)
            else :
                errs = bound_form.non_field_errors()
                for err in errs:
                    error(request,err)

        return TemplateResponse(request,self.template_name,{'form':bound_form})



class ActivateAccount(View):
    success_url = reverse_lazy('dj-auth:login')
    template_name = 'user/user_activate.html'



    def get(self,request,uidb64,token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError,ValueError,OverflowError,User.DoesNotExist):
            user = None

        if (user is not  None and token_generator.check_token(user,token)):
            user.is_active = True
            user.save()
            success(request,'user activated You may now login')
            return redirect(self.success_url)
        else:
            return TemplateResponse(request,self.template_name)

class ResendActivationEmail(
        MailContextViewMixin, View):
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('dj-auth:login')
    template_name = 'user/resend_activation.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()})

    @method_decorator(csrf_protect)
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            user = bound_form.save(
                **self.get_save_kwargs(request))
            if (user is not None
                    and not bound_form.mail_sent):
                errs = (
                    bound_form.non_field_errors())
                for err in errs:
                    error(request, err)
                if errs:
                    bound_form.errors.pop(
                        '__all__')
                return TemplateResponse(
                    request,
                    self.template_name,
                    {'form': bound_form})
        success(
            request,
            'Activation Email Sent!')
        return redirect(self.success_url)



class ProfileDetail(ProfilGetObjectMixin,DetailView):
    model = Profile


class ProfileUpdate(ProfilGetObjectMixin,UpdateView):
    model = Profile
    fields = ('about',)
    template_name_suffix = '_form_update'


class PublicProfileDetail(DetailView):
    model = Profile

