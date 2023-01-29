from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

# ...
def create_data():
    user = User.objects.create_user(
        username='vince',
        email='vince@test.com',
        password='testpass123'
    )

    vehicle = Vehicle(
        make='Make',
        model='Model',
        reg_number='1234',
        user=user
    )
    vehicle.save()

    origin = Place(name='Origin')
    origin.save()

    destination = Place(name='Destination')
    destination.save()


class TripApiTest(APITestCase):

    

    def test_create_trip(self):
        create_data()
        user = User.objects.get(pk=1)

        self.client.force_authenticate(user=user) # force authentication

        response = self.client.post('/api/v1/trips/', {
            'trip_date': str(date.today()),
            'origin_id': 1,
            'destination_id': 2,
            'vehicle_id': 1
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        trip = Trip.objects.get(pk=1)
        self.assertEqual(trip.origin.name, 'Origin')
        self.assertEqual(trip.destination.name, 'Destination')
        self.assertEqual(trip.trip_date, date.today())
        self.assertEqual(trip.user, user)
    def test_get_trips(self):
        create_data()
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=2)

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=date.today()
        )
        trip.save()

        response = self.client.get('/api/v1/trips/')
        self.assertEqual(json.loads(response.content), [
            {
                "id": 1,
                "url": "http://testserver/api/v1/trips/1/",
                "trip_date": str(date.today()),
                "num_seats": 1,
                "origin": {
                    "id": 1,
                    "name": "Origin"
                },
                "destination": {
                    "id": 2,
                    "name": "Destination"
                },
                "vehicle": {
                    "id": 1,
                    "url": "http://testserver/api/v1/vehicles/1/",
                    "make": "Make",
                    "model": "Model",
                    "reg_number": "1234",
                    "image": None,
                    "owner_url": "http://testserver/api/v1/users/1/"
                },
                "driver": {
                    "username": "vince",
                    "email": "vince@test.com",
                    "first_name": "",
                    "last_name": "",
                    "gender": "wont-say",
                    "birth_date": None,
                    "url": "http://testserver/api/v1/users/1/",
                    "profile_pic": None
                }
            }

        ])
