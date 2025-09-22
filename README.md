# Minivenmo API

A simple payment processing API built with FastAPI and SQLite, inspired by Venmo. This API allows users to create accounts, check balances, send payments to other users, and manage friend relationships.

## Features

- User account creation and management
- Balance checking and management
- Payment processing between users
- Friend management system
- Transaction history and activity feed
- Comprehensive test coverage

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hudrec/test-taller-python.git
   cd test-taller-python
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

The application uses SQLite with Peewee ORM. The database will be automatically created when you first run the application.

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## Running Tests

To run the test suite:
```bash
pytest test_api.py -v
```

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://127.0.0.1:8000/docs`
- Alternative documentation (ReDoc): `http://127.0.0.1:8000/redoc`

## API Endpoints

### Users
- `POST /create-user` - Create a new user
- `GET /users` - List all users
- `GET /users/{user_id}/activity` - Get user activity feed
- `POST /users/add-friend` - Add a friend

### Payments
- `POST /pay` - Send payment to another user

## Project Structure

- `main.py` - Main FastAPI application and route handlers
- `models.py` - Database models using Peewee ORM
- `database.py` - Database connection and initialization
- `test_api.py` - Test cases for the API endpoints
- `requirements.txt` - Project dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
