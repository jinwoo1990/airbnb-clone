from django import forms
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 중복이 많으므로 아래 clean method 로 통합
    # clean 으로 시작된 function 들은 cleaned_data 에 영향을 주도록 설계되어 있음
    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User does not exist")
    #
    # def clean_password(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password(password):
    #             return password
    #         else:
    #             raise forms.ValidationError("Password is wrong")
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User does not exist")

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                # clean 을 썼다면 cleaned_data 를 return 해야 함
                return self.cleaned_data
            else:
                # clean 하나로 function 을 구성했을 시 self.add_error 로 해야 error 발생 지점에 정확히 작동하게 할 수 있음
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


# class SignUpForm(forms.Form):
#     first_name = forms.CharField(max_length=80)
#     last_name = forms.CharField(max_length=80)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
#
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         try:
#             models.User.objects.get(email=email)
#             raise forms.ValidationError("User already exists with that email")
#         except models.User.DoesNotExist:
#             return email
#
#     # 선언된 순서대로 clean 되어 cleaned_data 에 담기게 되는데 password1 은 password 로 선언된 함수에서는 아직 정의되지 않아 더 밑에 있는
#     # password1 기준 함수로 작성해야 함
#     def clean_password1(self):
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")
#
#         if password != password1:
#             raise forms.ValidationError("Password confirmation does not match")
#         else:
#             return password
#
#     def save(self):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")
#
#         user = models.User.objects.create_user(email, email=email, password=password)
#
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # 선언된 순서대로 clean 되어 cleaned_data 에 담기게 되는데 password1 은 password 로 선언된 함수에서는 아직 정의되지 않아 더 밑에 있는
    # password1 기준 함수로 작성해야 함
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        username = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)
        user.username = username
        user.set_password(password)
        user.save()
