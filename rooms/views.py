# from datetime import datetime
# from math import ceil
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.core.paginator import Paginator, EmptyPage
# from . import models

from django.utils import timezone
from django.http import Http404
from django.views.generic import ListView, DetailView, View
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django_countries import countries
from . import models, forms


# def all_rooms(request):
#     # print(dir(request.GET))
#     # print(request.GET.get("page", 0))
#
#     # 이건 dictionary 기능 호출한 것, or 1 은 page 를 잘못 입력해도 최소 1을 보장하려고
#     page = int(request.GET.get("page", 1) or 1)
#     page_size = 10
#     limit = page_size * page
#     offset = limit - page_size
#     # django 는 lazy 해서 all() 싫행한 다음이 아닌 limit 까지 본 다음에 실행함
#     all_rooms_list = models.Room.objects.all()[offset:limit]
#     page_count = ceil(models.Room.objects.count() / page_size)
#
#     # template 코드에서는 파이썬의 모든 기능을 지원하지 않으므로 아예 여기서 만들어서 넘김
#     return render(request, "rooms/room_list.html",
#                   context={"rooms": all_rooms_list,
#                            "page": page,
#                            "page_count": page_count,
#                            "page_range": range(1, page_count + 1),
#                            })


# Paginator 를 이용하면 페이지 넘기는 기능을 엄청 간단하게 만들 수 있음
# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     # queryset 은 lazy 하므로 밑에처럼 하는 것은 틀만 만들고 데이터를 실제로 불러오지 않음
#     # 따라서 부하주지 않음 print() 이런 것 하기 전까지는
#     room_list = models.Room.objects.all()
#     # orphans 로 원래 페이지 크기인 10개보다 작을 때 orphans 수 이하의 갯수를 숨김 (페이지에 몇 개만 남는 것 방지, 그 전 페이지에 합쳐버림)
#     paginator = Paginator(room_list, 10, orphans=5)
#
#     try:
#         # get_page 는 좀 더 사용하기 편하게 많은 처리를 해줬고 page 는 각각 에러 상황을 지정해야 되지만 자유도가 높음
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/room_list.html", {"page": rooms})
#     except EmptyPage:
#         # redirect 를 하면 url 에 user가 page=2332339 이렇게 쳐도 / 로 다시 돌아가므로 깔끔
#         return redirect("/")


# ListView 만으로 모델을 지정해주고 template html 을 원하는 방식 (room_list) 로 지정해주면 작동
# class 가 동작하는 동안 사용할 수 있는 object_list 가 있고 이를 통해 page.object_list 할 필요도 없이 바로 활용 가능
# 너무 추상화가 많이 되어 있어 function based view 만을 써야 된다는 식의 논쟁이 있음
# class based view 는 정해진 일을 수행하는데 정말 좋음. 다만, 커스터마이즈된 기능을 쓰고 싶다면 function based view 가 좋음
class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"

    context_object_name = "rooms"

    # html 에서는 page_obj 로 이미 정의된 page 객체를 바탕으로 화면을 구성할 수 있음

    # ListView 클래스에 정의된 객체 외에 추가적인 객체를 정의해서 template 에서 활용 가능
    # def get_context_data(self, **kwargs):
    #     # 여기서 상속을 받아야 ListView 에서 정의된 모든 객체들을 쓸 수 있음
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now()
    #     context["now"] = now
    #     return context


# 짧고 paginate 할 것도 없어 그냥 이렇게 function based view 로 써도 됨
# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/room_detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         # debug = False 해야 페이지 나옴
#         raise Http404()


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


# django form API 를 이용하지 않는 방식
# def search(request):
#     city = request.GET.get("city", "anywhere")
#     city = str.capitalize(city)
#     country = request.GET.get("country", "KR")
#     room_type = int(request.GET.get("room_type", 0))
#     price = int(request.GET.get("price", 0))
#     guests = int(request.GET.get("guests", 0))
#     bedrooms = int(request.GET.get("bedrooms", 0))
#     beds = int(request.GET.get("beds", 0))
#     baths = int(request.GET.get("baths", 0))
#     instant = bool(request.GET.get("instant", False))
#     superhost = bool(request.GET.get("superhost", False))
#     s_amenities = request.GET.getlist("amenities")
#     s_facilities = request.GET.getlist("facilities")
#
#     # 입력할 것
#     form = {
#         "city": city,
#         "s_country": country,
#         "s_room_type": room_type,
#         "price": price,
#         "guests": guests,
#         "bedrooms": bedrooms,
#         "beds": beds,
#         "baths": baths,
#         "instant": instant,
#         "superhost": superhost,
#         "s_amenities": s_amenities,
#         "s_facilities": s_facilities,
#     }
#
#     room_types = models.RoomType.objects.all()
#     amenities = models.Amenity.objects.all()
#     facilities = models.Facility.objects.all()
#
#     # db 에서 나오는 것
#     choices = {
#         "countries": countries,
#         "room_types": room_types,
#         "amenities": amenities,
#         "facilities": facilities,
#     }
#
#     filter_args = {}
#
#     if city != "Anywhere":
#         filter_args["city__startswith"] = city
#
#     filter_args["country"] = country
#
#     if room_type != 0:
#         # foreign key 이므로 pk 로 접근
#         filter_args["room_type__pk"] = room_type
#
#     if price != 0:
#         filter_args["price_lte"] = price
#
#     if guests != 0:
#         filter_args["guests_gte"] = guests
#
#     if bedrooms != 0:
#         filter_args["bedrooms_gte"] = bedrooms
#
#     if beds != 0:
#         filter_args["beds_gte"] = beds
#
#     if baths != 0:
#         filter_args["baths_gte"] = baths
#
#     if instant is True:
#         filter_args["instant_book"] = True
#
#     if superhost is True:
#         filter_args["host__superhost"] = True
#
#     if len(s_amenities) > 0:
#         for s_amenity in s_amenities:
#             filter_args["amenities__pk"] = int(s_amenity)
#
#     if len(s_facilities) > 0:
#         for s_facility in s_facilities:
#             filter_args["facilities__pk"] = int(s_facility)
#
#     rooms = models.Room.objects.filter(**filter_args)
#
#     return render(request,
#                   "rooms/search.html",
#                   {**form, **choices, "rooms": rooms}
#                   )

class SearchView(View):
    def get(self, request):
        # request.GET 을 인자로 주면 값을 기억함 + bounded 된 데이터를 바탕으로 validation 을 진행
        # form = forms.SearchForm(request.GET)

        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bathrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price_lte"] = price

                if guests is not None:
                    filter_args["guests_gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms_gte"] = bedrooms

                if beds is not None:
                    filter_args["beds_gte"] = beds

                if baths is not None:
                    filter_args["baths_gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                # cleaned_data 에서는 전부 queryset 으로 정리되어 있으므로 pk 같은 식으로 접근할 필요 없이 이렇게 활용
                for amenity in amenities:
                    filter_args["amenities"] = int(amenity)

                for facility in facilities:
                    filter_args["facilities"] = int(facility)

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(request,
                              "rooms/search.html",
                              {"form": form, "rooms": rooms})
        else:
            form = forms.SearchForm()

        # url 을 사용자가 이상하게 조작할 수도 있기 때문에 여기에 항상 return 하게 넣어줌 (에러라도 보여줌)
        return render(request,
                      "rooms/search.html",
                      {"form": form})
