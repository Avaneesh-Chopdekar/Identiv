# Identiv

A Face Recognition Security System

## Install

Clone the repository into your system

```bash
git clone https://github.com/Avaneesh-Chopdekar/identiv.git
```

### With Docker

Make sure you have created a `.env` file just like `.env.example` and filled with relevant credentials.

Now run the command below to start the application

> If you are running this for the first time, make sure you add `--build` in the command
>
> `docker-compose up --build`

```bash
docker-compose up
```

The application will be available at `http://127.0.0.1:8000`

To stop the application, press CTRL + C in the terminal

### Without Docker

First install all the necessary dependencies for this project

> If you are using a Windows device, make sure you have Visual Studio installed with Desktop development with C++ selected.

```bash
pip install -r requirements.txt
```

Make sure you have created a `.env` file just like `.env.example` and filled with relevant credentials.

Now run the command below to start the application

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

To stop the application, press CTRL + C in the terminal

## Tech Stack

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Docker](https://www.docker.com/)
- [face_recognition](https://pypi.org/project/face-recognition/)
- [opencv](https://pypi.org/project/opencv-python/)
