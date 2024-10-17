# Contributing to Identiv

Thank you for your interest in contributing to Identiv! This document provides guidelines to help you contribute effectively.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How Can You Contribute?](#how-can-you-contribute)
3. [Reporting Issues](#reporting-issues)
4. [Submitting Pull Requests](#submitting-pull-requests)
5. [Setting Up the Development Environment](#setting-up-the-development-environment)
6. [Writing Tests](#writing-tests)
7. [Code Style](#code-style)
8. [PostHog & Sentry Integration](#posthog--sentry-integration)
9. [Getting Help](#getting-help)

## Code of Conduct

This project adheres to the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code. If you experience or witness unacceptable behavior, please report by creating an issue.

## How Can You Contribute?

There are many ways to contribute:
- **Bug Reports**: If you encounter any bugs, submit an issue with a detailed description and steps to reproduce.
- **Feature Requests**: Have an idea? Submit a request for a new feature.
- **Code Contributions**: Fixing bugs or adding features is a great way to help improve the project.
- **Documentation**: Help keep our documentation clear and up-to-date.
- **Tests**: Write unit tests to ensure our models and forms work as expected.

## Reporting Issues

- Search the [issue tracker](https://github.com/Avaneesh-Chopdekar/Identiv/issues) first to make sure your issue hasn’t been reported.
- Provide a clear and descriptive title.
- Describe the exact steps that led to the issue and any relevant code, logs, or screenshots.
- Label the issue appropriately (bug, enhancement, question, etc.).

## Submitting Pull Requests

When you're ready to contribute code:
1. Fork the repository.
2. Clone the forked repository to your local machine.
3. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes.
5. Add or update tests to cover your changes.
6. Run tests locally to ensure everything works:
   ```bash
   python manage.py test
   ```
7. Commit your changes with a meaningful message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```
8. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
9. Create a Pull Request (PR) from your branch to the master repository.
10. The PR will be reviewed by a maintainer, and you may be asked to make additional changes before it can be merged.

## Setting Up the Development Environment

Follow these steps to set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Avaneesh-Chopdekar/Identiv.git
   cd Identiv
   ```

2. **Set up Docker**:
   Make sure you have Docker and Docker Compose installed on your system.

3. **Build and run the containers**:
   ```bash
   docker-compose up --build
   ```

4. **Run migrations**:
   Inside the running container:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Run the development server**:
   The app will be accessible at `http://localhost:8000`.

## Writing Tests

Tests are crucial for ensuring that the application works as expected. We encourage you to write unit tests for any new feature or bug fix.

- **Unit Tests**: Make sure to cover all models, forms, and critical functions.
- Run the tests:
  ```bash
  docker-compose exec web python manage.py test
  ```

If you're unsure about writing tests, feel free to ask for guidance in your pull request.

## Code Style

This project follows [PEP8](https://www.python.org/dev/peps/pep-0008/) guidelines. We use `flake8` to check for code style issues.

- Before submitting a PR, make sure your code passes linting:
  ```bash
  pip install flake8
  flake8
  ```

## PostHog & Sentry Integration

This project uses **PostHog** for analytics and **Sentry** for error tracking. If you’re working on a feature that involves these tools, ensure that they are correctly integrated by referring to the following:

- [PostHog Documentation](https://posthog.com/docs)
- [Sentry Documentation](https://docs.sentry.io/)

Make sure that the environment variables for these services are correctly set in `.env` or `docker-compose.yml` files.

## Getting Help

If you need help or have any questions:
- Open an issue on [GitHub](https://github.com/Avaneesh-Chopdekar/Identiv/issues).

We are happy to assist you!

---

Thank you for contributing to **Identiv!** We value your time and effort in improving the project.

### Key Points of the `CONTRIBUTING.md`:
- **Code of Conduct**: Link to the Code of Conduct and encourage adherence.
- **How to Contribute**: Options for contributing like reporting issues, writing tests, etc.
- **Development Environment Setup**: Steps to get Docker containers up and running for local development.
- **Tests and Code Style**: Guidelines for writing unit tests and ensuring code follows PEP8.
- **PostHog and Sentry**: Mentions the integration of PostHog and Sentry, pointing contributors to their docs.
- **Help**: Ways to get help, through GitHub or an email contact.
