# Identiv - Face Recognition and Organization Management System

This project is a Django-based application that provides face recognition login functionality and allows organizations to manage custom registration fields, view login logs, and handle notifications for registration approval. It integrates PostHog for analytics and Sentry for error tracking.

## Features

### Organization Features:

1. **Create an Account:** Organizations can create their own accounts.
2. **Custom Registration Fields:** Organizations can define custom registration fields, including radio buttons and checkboxes, for people registering under them.
3. **Field Options Management:** Organizations can add options for radio and checkbox fields.
4. **View and Filter People:** Organizations can view all registered people and filter them based on the custom registration fields (radio/checkbox).
5. **Login Logs:** Organizations can view login logs of registered people, including details of who logged in and when.
6. **Notification Management:**
   - View pending registration notifications.
   - Approve or reject registration requests.
   - If a person’s request is rejected, they are blacklisted and cannot log in until removed from the blacklist.

### People Features:

1. **Custom Registration:** People can register using the custom fields set by the organization.
2. **Login Restrictions:** People cannot log in until their registration request is approved by the organization.
3. **Blacklist:** If a person is blacklisted by an organization, they cannot log in until they are unblacklisted.

### Technology Stack:

- **Python 3.10**
- **Django 5.1**
- **Postgres with pg-vector for facial embeddings**
- **Docker**
- **PostHog Analytics Integration**
- **Sentry Error Tracking**
- **face_recognition library**

## Prerequisites

Make sure you have the following installed:

- Docker
- Docker Compose

## Setup and Installation

### 1. Clone the repository:

```bash
git clone https://github.com/Avaneesh-Chopdekar/Identiv.git
cd Identiv
```

### 2. Set up the environment variables:

Rename `.env.example` to `.env` and fill in the necessary environment variables:

```bash
cp .env.example .env
```

- **ENVIRONMENT:** Set to `dev` for development or `prod` for production.
- **TIME_ZONE:** Your time zone (e.g., `Asia/Kolkata`).
- **SECRET_KEY:** A secret key for your Django application.
- **Postgres:** Set up the database credentials.
- **SMTP:** Set up email credentials for notifications.
- **PostHog:** Set your PostHog API key and host for analytics.
- **Sentry:** Set your Sentry DSN for error tracking.

### 3. Build and run the application using Docker Compose:

```bash
docker-compose up --build
```

This will start the application and expose it at `http://localhost:8000`.

### 4. Run Migrations:

```bash
docker-compose exec web python manage.py migrate
```

### 5. Collect static files:

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### 6. Run Unit Tests:

To ensure the models and forms are functioning correctly, run unit tests:

```bash
docker-compose exec web python manage.py test app dashboard
```

## PostHog Analytics Integration

This project integrates with PostHog for tracking user interactions. Ensure the following environment variables are set correctly in your `.env` file:

- `POSTHOG_API_KEY`
- `POSTHOG_HOST`

PostHog events will automatically be captured in the application.

## Sentry Error Tracking

Sentry is integrated to track and report errors. To enable it, ensure the following environment variable is set in your `.env` file:

- `SENTRY_DSN`

Errors will be logged to Sentry, helping you monitor and resolve issues quickly.

## Features Breakdown

### Organization Workflow:

1. **Creating an Organization Account:**
   - The organization signs up and sets up registration fields.
2. **Custom Fields for Registration:**

   - Organizations define which custom fields (text, bigtext, radio, checkbox) are required for registration.

3. **Viewing and Managing Registrations:**
   - Filter registered people based on these custom fields.
4. **Handling Notifications:**
   - The organization receives notifications for new registration requests.
   - Approve or reject these requests.
   - Rejected requests result in the person being blacklisted, preventing future login attempts until removed from the blacklist.

### People Workflow:

1. **Registration:**
   - People can register based on the custom fields set by the organization.
2. **Login Restrictions:**

   - Login is only enabled once the organization approves the registration request.

3. **Blacklist Handling:**
   - People who are blacklisted by the organization cannot log in until the blacklist status is cleared.

## Running the Development Server

Once everything is set up, run the development server using Docker:

```bash
docker-compose up
```

The application will be accessible at `http://localhost:8000`.

## Running Unit Tests

To ensure the integrity of your models and forms, you can run unit tests:

```bash
docker-compose exec web python manage.py test
```

This will run all the test cases for models and forms within your Django app.

## License

This project is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3. See the [LICENSE](LICENSE) file for more information.

## Contributing

If you wish to contribute to this project, please submit a pull request or open an issue for discussion.
