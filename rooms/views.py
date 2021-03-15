from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from . import models


def all_rooms(request):
    all_rooms_list = models.Room.objects.all()
    now = datetime.now()
    hungry = True

    # return HttpResponse(content=f"<h1>{now}</h1>")
    return render(request, "rooms/home.html",
                  context={"rooms": all_rooms_list}
                  )
