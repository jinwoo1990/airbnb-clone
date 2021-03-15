import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates many users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many users do you want to creates",
            )

    def handle(self, *args, **options):
        number = options.get("number")

        # seeder 는 foreign key 를 참조할 수 없어 처리
        seeder = Seed.seeder()

        # 실제로 데이터베이스가 크면 .objects.all 로 가져오지 않음
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()

        seeder.add_entity(room_models.Room, number, {
            "name": lambda x: seeder.faker.address(),
            "host": lambda x: random.choice(all_users),
            "room_type": lambda x: random.choice(room_types),
            "guests": lambda x: random.randint(1, 20),
            "price": lambda x: random.randint(1, 300),
            "beds": lambda x: random.randint(1, 5),
            "bedrooms": lambda x: random.randint(1, 5),
            "baths": lambda x: random.randint(1, 5),
        })
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))

        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(5, 20)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"/room_photos/{random.randint(1, 21)}.jpg",
                )

        for a in amenities:
            magic_number = random.randint(0, 15)
            if magic_number % 2 == 0:
                # many to many fields 에서 추가하는 방법
                room.amenities.add(a)

        for f in facilities:
            magic_number = random.randint(0, 15)
            if magic_number % 2 == 0:
                room.facilities.add(f)

        for r in rules:
            magic_number = random.randint(0, 15)
            if magic_number % 2 == 0:
                room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created"))
