from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()

    pass


class PhotoInline(admin.TabularInline):

    model = models.Photo

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    # admin 안에 admin 을 집어 넣음. room admin 에서 연결된 foreign key 를 바탕으로 photo 를 만들 수 있음
    inlines = (PhotoInline,)

    # section 나누기
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")}
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")}
        ),
        (
            "Spaces",
            {"fields": ("guests", "beds", "bedrooms", "baths")}
        ),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # hide 할 수 있는 섹션으로 만들기
                "fields": ("amenities", "facilities", "house_rules")
            }
        ),
        (
            "Last Details",
            {"fields": ("host",)}
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = ("name", "price", "bedrooms")

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "city",
        "amenities",
        "facilities",
        "house_rules",
        "country",
    )

    # user 의 긴 리스트를 보는 게 아니라 검색도 하고 1,2 처럼 key 로 검색할 수 있게 함
    raw_id_fields = ("host",)

    # search option 으로 ^ 을 주면 startswith 로 검색, 아니면 icontatins 인데 django 문서에 나와 있음
    search_fields = ("=city", "^host__username")  # 복수 필드로 검색

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # def save_model(self, request, obj, form, change):
    #     send_mail()
    #     super().save_model(request, obj, form, change)

    # self 는 클래스 자신, obj 는 row
    def count_amenities(self, obj):
        # print(obj.amenities.count())
        return obj.amenities.count()

    # 표시되는 컬럼명을 바꿀 수 있음
    # count_amenities.short_description = "hello sexy!"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail",)

    def get_thumbnail(self, obj):
        # 보안으로 이런 식으로 접근 하는 것은 안 되게 함. 그냥 텍스트만 보임
        # mark_safe 하면 보여짐
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"

    pass
