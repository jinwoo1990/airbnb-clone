from datetime import datetime
from math import ceil
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage
from . import models


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
#     return render(request, "rooms/home.html",
#                   context={"rooms": all_rooms_list,
#                            "page": page,
#                            "page_count": page_count,
#                            "page_range": range(1, page_count + 1),
#                            })


# Paginator 를 이용하면 페이지 넘기는 기능을 엄청 간단하게 만들 수 있음
def all_rooms(request):
    page = request.GET.get("page", 1)
    # queryset 은 lazy 하므로 밑에처럼 하는 것은 틀만 만들고 데이터를 실제로 불러오지 않음
    # 따라서 부하주지 않음 print() 이런 것 하기 전까지는
    room_list = models.Room.objects.all()
    # orphans 로 원래 페이지 크기인 10개보다 작을 때 orphans 수 이하의 갯수를 숨김 (페이지에 몇 개만 남는 것 방지, 그 전 페이지에 합쳐버림)
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        # get_page 는 좀 더 사용하기 편하게 많은 처리를 해줬고 page 는 각각 에러 상황을 지정해야 되지만 자유도가 높음
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        # redirect 를 하면 url 에 user가 page=2332339 이렇게 쳐도 / 로 다시 돌아가므로 깔끔
        return redirect("/")


class