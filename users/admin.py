from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


# UserAdmin 으로 extension 하면 user 는 충분히 잘 작성된 것을 사용할 수 있음
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    # # admin 창에서 나열한 정보를 표처럼 리스트업
    # list_display = ("username", "gender", "email", "language", "currency", "superhost")
    #
    # # admin 창에서 나열한 정보로 필터 가능하게
    # list_filter = ("language", "currency", "superhost",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "login_method"
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )
