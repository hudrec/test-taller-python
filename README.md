# Minivenmo API

A simple payment processing API built with FastAPI and SQLite, inspired by Venmo. This API allows users to create accounts, check balances, and send payments to other users.

## Features

- User account creation
- Balance management
- Payment processing between users
- Credit card integration for overdraft protection
- Transaction history feed

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
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

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://127.0.0.1:8000/docs`
- Alternative documentation: `http://127.0.0.1:8000/redoc`

## Endpoints

### Create User
- **POST** `/create-user`
  - Request body: `{ "name": "John Doe", "balance": 100.0 }`
  - Creates a new user with the specified name and initial balance

### Make a Payment
- **POST** `/pay`
  - Request body: `{ "payer": 1, "amount": 50.0, "receiver": 2, "reason": "Dinner" }`
  - Processes a payment from one user to another
  - If the payer doesn't have enough balance, it will attempt to charge their credit card

## Database

The application uses SQLite with the database file `minivenmo.db` which is automatically created on first run.

## Project Structure

- `main.py` - Main FastAPI application and endpoints
- `models.py` - Database models and business logic
- `requirements.txt` - Python dependencies
- `.gitignore` - Specifies intentionally untracked files to ignore

## License

This project is licensed under the MIT License - see the LICENSE file for details.
