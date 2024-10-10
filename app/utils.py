import cv2
import numpy as np
import base64
import face_recognition
from pgvector.django import L2Distance

from app.models import Person


def find_person_by_embedding(face_embedding, organization=None):

    if (
        Person.objects.count() == 0
        or Person.objects.filter(organizations=organization).count() == 0
    ):
        return None

    if organization is None:
        person = Person.objects.order_by(
            L2Distance("face_embedding", face_embedding)
        ).first()
    else:
        person = (
            Person.objects.filter(organizations=organization)
            .order_by(L2Distance("face_embedding", face_embedding))
            .first()
        )

    is_match = face_recognition.compare_faces([person.face_embedding], face_embedding)

    if is_match[0]:
        return person
    else:
        # If no match found or similarity is below threshold
        return None


def extract_image_from_data_uri(data_uri):
    """Extracts the image data from a data URI and returns it as a NumPy array.

    Args:
        data_uri (str): The data URI string.

    Returns:
        np.ndarray: The extracted image data as a NumPy array.
    """

    try:
        # Split the data URI into its components
        _, _, data = data_uri.partition(",")

        # Decode the base64-encoded data
        image_data = base64.b64decode(data)

        # Convert the image data to a NumPy array
        image_array = np.frombuffer(image_data, np.uint8)

        # Decode the image using OpenCV
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        return image
    except Exception as e:
        print(f"Error extracting image from data URI: {e}")
        return None
