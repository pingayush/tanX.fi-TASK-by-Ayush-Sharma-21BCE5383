# tanX.fi-TASK-by-Ayush-Sharma-21BCE5383

# Price Alert Application

This application allows users to create price alerts for cryptocurrencies. When the target price is achieved, the application sends an email notification to the user.

## Features

- Create a price alert.
- Delete a price alert.
- List all created alerts with filter options.
- User authentication with JWT tokens.
- Real-time price updates using Binance WebSocket.
- Email notifications for triggered alerts.
- Caching for fetching alerts.
- Dockerized setup with Celery and Redis for background tasks.

## Technologies Used

- Django
- Django Rest Framework
- Postman
- Celery
- Redis
- PostgreSQL
- Docker
- Binance WebSocket
- SMTP for sending emails

## Prerequisites

- Docker and Docker Compose installed on your machine.

##Project Structure
price_alert/
├── alerts/
├── price_alert/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
├── price_alerts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── views.py
│   ├── urls.py
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt

