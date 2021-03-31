from datetime import datetime
from math import ceil
from django.shortcuts import render
from django.http import HttpResponse
from . import models


def all_rooms(request):
    # print(dir(request.GET))
    # print(request.GET.get("page", 0))

    # 이건 dictionary 기능 호출한 것, or 1 은 page 를 잘못 입력해도 최소 1을 보장하려고
    page = int(request.GET.get("page", 1) or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    # django 는 lazy 해서 all() 싫행한 다음이 아닌 limit 까지 본 다음에 실행함
    all_rooms_list = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)

    # template 코드에서는 파이썬의 모든 기능을 지원하지 않으므로 아예 여기서 만들어서 넘김
    return render(request, "rooms/home.html",
                  context={"rooms": all_rooms_list,
                           "page": page,
                           "page_count": page_count,
                           "page_range": range(1, page_count + 1),
                           })
