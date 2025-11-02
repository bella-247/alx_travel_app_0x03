## Background Task Management with Celery and RabbitMQ

This project configures Celery with RabbitMQ to handle background email notifications.

### Key Features
- RabbitMQ as message broker
- Celery for asynchronous task processing
- Automatic booking confirmation email

### Important Files
- `alx_travel_app/settings.py` – Celery & email configs
- `alx_travel_app/celery.py` – Celery app setup
- `listings/tasks.py` – Email task definition
- `listings/views.py` – Task trigger on booking creation


# ALX Travel App

## Overview
ALX Travel App is a Django-based web application for managing travel property listings, bookings, and reviews. It provides a platform for users to browse available properties, make bookings, and leave reviews for their stays.

## Features
- Property listing management
- Booking system for guests
- Review system for properties
- Admin interface for managing listings, bookings, and reviews
- RESTful API endpoints (using Django REST Framework)
- Docker support for easy deployment

## Project Structure
- `alx_travel_app/` - Main Django project configuration
- `listings/` - App for property listings, bookings, and reviews
- `db.sqlite3` - Default SQLite database
- `docker-compose.yaml` - Docker configuration
- `requirement.txt` - Python dependencies

## Setup Instructions
1. **Clone the repository:**
	```sh
	git clone <repo-url>
	cd alx_travel_app_0x00
	```
2. **Install dependencies:**
	```sh
	pip install -r requirement.txt
	```
3. **Apply migrations:**
	```sh
	python manage.py migrate
	```
4. **Run the development server:**
	```sh
	python manage.py runserver
	```
5. **Access the app:**
	Visit `http://127.0.0.1:8000/` in your browser.

## API Endpoints
The app exposes RESTful endpoints for listings, bookings, and reviews. See the API documentation for details.

## Docker Usage
To run the app using Docker:
```sh
docker-compose up --build
```

## License
This project is licensed under the MIT License.
# alx_travel_app_0x00