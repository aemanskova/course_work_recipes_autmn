
from django.contrib.auth import get_user_model
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsMeOrReadOnly
from users.serializers import UserListSerializer, UserDetailSerializer,UserSerializer
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from .pagination import BasePagination
from users.forms import EditProfileForm, SignupForm
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = BasePagination
    
    @action(methods=['GET'], detail=False)
    def get_staff(self, request, **kwargs):

        queryset = self.get_queryset().filter(Q(is_staff=True))
        serializer = UserSerializer(queryset, many=True)
        data = dict()
        data['data'] = serializer.data
        return Response(data)
    
    

    @action(methods=['POST','GET'], detail=True)
    def toggle_staff(self, request, **kwargs):
        user = self.get_object()
        user.is_staff = not(user.is_staff)
        
        user.save()
        return Response(f'Статус персонала {user.is_staff}')

class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsMeOrReadOnly, IsAuthenticated]
    serializer_class = UserDetailSerializer


class CurrentUser(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user


class UsersListView(TemplateView):
    """
    Отображает список пользователей

    Context:
        users (User[]): QuerySet, содержащий экземпляры класса User

    Template:
        template_name: 'users/users_list.html'

    """

    template_name = 'users/users_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.only('id', 'username')
        context['users'] = users
        return context


@method_decorator(login_required, name='dispatch')
class UserDetailView(TemplateView):
    """
    Отображает страницу пользователя (User)

    Context:
        user (User): экземпляр класса User

    Template:
        template_name: 'users/users_list.html'

    """
    template_name = 'users/user_detail.html'

    def get(self, request, id: int, *args, **kwargs):
        if request.user.id == id:
            return redirect('users:profile')
        else:
            return render(request,
                          self.template_name,
                          self.get_context_data(id))

    def get_context_data(self, id: int, **kwargs):
        context = super().get_context_data(**kwargs)
        user: User = get_object_or_404(User.objects.only('email', 'username'), pk=id)
        context['user'] = user
        return context


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'users/profile.html'
    form_class = EditProfileForm

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template_name,
                      self.get_context_data(request))

    def post(self, request, *args, **kwargs):
        user: User = get_object_or_404(User.objects.only('email', 'username'),
                                       pk=request.user.id)

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid() and form.validate_all(request.user):
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['login']
            user.save()

            return redirect('users:profile')

        return render(request,
                      self.template_name,
                      self.get_context_data(request))

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)

        user: User = get_object_or_404(User.objects.only('email', 'username'),
                                       pk=request.user.id)

        initial_form_data = {
            'email': user.email,
            'login': user.username,
        }
        form = self.form_class(request.POST or None,
                               request.FILES or None,
                               initial=initial_form_data)

        if form.is_valid():
            form.validate_all(user)

        context['user'] = user
        context['form'] = form

        return context


class SignupView(TemplateView):
    template_name = 'users/signup.html'
    form_class = SignupForm

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template_name,
                      self.get_context_data(request))

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(request)

        form = context['form']

        if form.is_valid() and form.check_passwords_match():
            user: User = User.objects.create_user(
                username=form.cleaned_data['login'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )

            login(request, user)

            return redirect('homepage:home')

        return render(request,
                      self.template_name,
                      self.get_context_data(request))

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(request.POST or None)
        context['form'] = form
        form.is_valid() and form.check_passwords_match()
        return context
