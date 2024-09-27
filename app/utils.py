import cv2
import numpy as np
import dlib
import base64
import face_recognition

from app.models import Person


def find_person_by_embedding(face_embedding):
    persons = Person.objects.all()

    for person in persons:
        # person.face_embedding is assumed to be a vector from pgVector field
        stored_embedding = np.array(
            person.face_embedding
        )  # Convert the stored vector back to numpy array
        similarity = face_recognition.compare_faces([stored_embedding], face_embedding)

        if similarity[0]:
            return person

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
