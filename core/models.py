from django.db import models


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    # 추가할 때 생성 날짜
    created = models.DateTimeField(auto_now_add=True)
    # save 할 때마다 새로운 날짜
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # model 인데 데이터베이스에 안 들어가고 다른 곳에서 extends 하기 위한 모델
        abstract = True
