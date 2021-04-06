from django.urls import path
from rooms import views as room_views

app_name = "core"

# urlpatterns 에 들어가는 값은 class 일 수 없음
# as_view()로 function 의 형식으로 집어넣어야 함
urlpatterns = [
    path("", room_views.HomeView.as_view(), name="home")
]


