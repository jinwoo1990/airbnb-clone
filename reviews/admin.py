from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """ Review Admin Definition """

    # model 의 __str__ 과 rating_average 를 각각 보여줌, __str__ 써서 참조 가능
    list_display = ("__str__", "rating_average")

    pass
