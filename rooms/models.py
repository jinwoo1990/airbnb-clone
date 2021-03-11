from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"
        ordering = ["-created"]

    pass


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"

    pass


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"

    pass


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"

    pass


class Photo(core_models.TimeStampedModel):
    """ HouseRule Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    # 아래 코드는 class 위치 때문에 에러
    # room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # django 는 아래와 같이 "Room" 으로 작성하면 코드의 아래쪽에 있더라도 불러올 수 있음
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # 다른 모델 참조 (room 에서 연결이 시작됨, many to one relationship, many rooms to one user, room 은 하나의 유저만 가짐)
    # Foreign key 로 user 의 id 를 가르키고 이것으로 user 의 정보를 참조
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    # many to many (여러가지 room_type 을 가질 수 있음)
    amenities = models.ManyToManyField("Amenity", blank=True)
    facilities = models.ManyToManyField("Facility", blank=True)
    house_rules = models.ManyToManyField("HouseRule", blank=True)

    def __str__(self):
        return self.name
