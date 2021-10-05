from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse

from common.views import CommonContextMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserProfileEditForm
from users.models import User


class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'


class UserRegistrationView(CommonContextMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрировались!'
    title = 'GeekShop - Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save()
            if self.send_verify_mail(user):
                messages.success(request, 'Вы успешно зарегистрировались!')
                return redirect(self.success_url)

            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})

    def send_verify_mail(self, user):
        verify_link = reverse_lazy('users:verify', args=[user.email, user.activation_key])

        title = f'Для активации учетной записи {user.username} пройдите по ссылке'

        messages = f'Для подтверждения учетной записи {user.username} пройдите по ссылке: \n{settings.DOMAIN_NAME}' \
                   f'{verify_link}'

        return send_mail(title, messages, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user.activation_key == activation_key and not user.is_activation_key_expires():
                user.is_active = True
                user.save()
                auth.login(self, user)
                return render(self, 'products/index.html')
            else:
                print(f'error activation user: {user}')
                return render(self, 'users/verification.html')
        except Exception as err:
            print(f'error activation user : {err.args}')
            return HttpResponseRedirect(reverse('index'))


#class UserProfileView(CommonContextMixin, UpdateView):
#    model = User
#    form_class = UserProfileForm
#    template_name = 'users/profile.html'
#    title = 'GeekShop - Личный кабинет'

#    def get_success_url(self):
#        return reverse_lazy('users:profile', args=(self.object.id,))

# реализовано через контексный процессор
#    def get_context_data(self, **kwargs):
#        context = super(UserProfileView, self).get_context_data(**kwargs)
#        context['baskets'] = Basket.objects.filter(user=self.object)
#        return context


class UserLogoutView(LogoutView):
    pass

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'title': 'GeekShop - Авторизация', 'form': form}
#     return render(request, 'users/login.html', context)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегестрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
#     context = {'title': 'GeekShop - Регистрация', 'form': form}
#     return render(request, 'users/register.html', context)


@transaction.atomic
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        profile_form = UserProfileEditForm(data=request.POST, instance=user.shopuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=user)
        profile_form = UserProfileEditForm(instance=user.shopuserprofile)
    context = {
        'title': 'GeekShop - Личный кабинет',
        'form': form,
        'profile_form': profile_form,
#        'baskets': Basket.objects.filter(user=user),
    }
    return render(request, 'users/profile.html', context)



