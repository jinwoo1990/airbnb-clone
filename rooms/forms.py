from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    # models 처럼 사용하는데 forms. 으로 시작하면 됨
    # widgets 을 통해 표시되는 형식을 바꿀 수 있음 (widgets=forms.Textarea)
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False,
        empty_label="Any kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    # help text 를 모델에 붙이면 admin 에 help text 로 보이고 form 에 붙이면 form 화면에 나옴
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    pass
