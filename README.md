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

