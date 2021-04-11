from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


# View 를 이용한 방법
# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "itn@las.com"})
#
#         return render(request, "users/login.html", {"form": form})
#
#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


# 많은 부분이 자동 구현되어 있음, 포맷만 맞추면 됨
# FormView 대신 LoginView 도 있는데 이건 username 과 password 조합을 강제해서 강의자는 추천 x
class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    # View 를 load 할 때 바로 로드하지 않고 lazy 하게 해야 에러 발생 안 함
    success_url = reverse_lazy("core:home")
    initial = {"email": "admin@gmail.com"}

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(self.request, username=email, password=password)
            if user is not None:
                login(self.request, user)
            return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "admin",
        "last_name": "a",
        "email": "admin@gmail.com"
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
