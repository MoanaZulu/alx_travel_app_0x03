# alx_travel_app_0x02

## Objective
Integrate the Chapa API for handling payments in a Django travel booking app.

## Features
- Secure payment initiation via Chapa API
- Verification of payment status
- Payment model for tracking transactions
- Confirmation emails via Celery
- Sandbox testing for safe integration

## Setup
1. Duplicate `alx_travel_app_0x01` into `alx_travel_app_0x02`.
2. Add `CHAPA_SECRET_KEY` to `.env`.
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate




# alx_travel_app_0x03

This project configures **Celery with RabbitMQ** to handle background tasks and implements an **email notification feature** for bookings.

## Features
- Celery worker setup with RabbitMQ broker
- Asynchronous booking confirmation emails
- Django email backend integration

## How to Run
1. Start RabbitMQ: `docker run -d -p 5672:5672 rabbitmq:latest`
2. Run Celery worker: `celery -A alx_travel_app worker -l info`
3. Run Django server: `python manage.py runserver`
