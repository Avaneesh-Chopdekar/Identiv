from django.test import TestCase
from app.models import Person
from face_recognition import compare_faces
import random
import decimal


class PersonModelTest(TestCase):
    def test_create_person(self):
        """Test creating a person"""

        # Generate a random decimal (like 1.xx) to populate the face_embedding field
        random_decimal = float(decimal.Decimal(random.randrange(101, 199)) / 100)

        first_name = "John"
        last_name = "Doe"
        face_embedding = [random_decimal for _ in range(128)]
        person = Person.objects.create(
            first_name=first_name,
            last_name=last_name,
            face_embedding=face_embedding,
        )

        self.assertEqual(person.first_name, first_name)
        self.assertEqual(person.last_name, last_name)
        self.assertListEqual(person.face_embedding, face_embedding)
