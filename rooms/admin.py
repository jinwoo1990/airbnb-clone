from django.contrib import admin
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


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    # section 나누기
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")}
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

    # search option 으로 ^ 을 주면 startswith 로 검색, 아니면 icontatins 인데 django 문서에 나와 있음
    search_fields = ("=city", "^host__username")  # 복수 필드로 검색

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # self 는 클래스 자신, obj 는 row
    def count_amenities(self, obj):
        # print(obj.amenities.count())
        return obj.amenities.count()

    # 표시되는 컬럼명을 바꿀 수 있음
    # count_amenities.short_description = "hello sexy!"

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass
