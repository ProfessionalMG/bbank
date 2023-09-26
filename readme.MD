# BBank: Simple Banking Application

Welcome to BBank! BBank is a streamlined banking application that provides functionalities such as account creation,
deposit and withdrawal operations, and viewing account balances.

## Features

- **Account Management**: Easily create, verify, and manage your bank account.
- **Transactions**: Deposit and withdraw money with ease.
- **Account Balance**: View your current account balance anytime.
- **Secure Authentication**: Robust authentication using JWT.

## Installation

Follow the steps below to get BBank up and running:

1. **Clone the Repository**:

```bash
git clone [repository_url]
```

2. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

3. **Run the Application**:

```bash
python manage.py runserver
```

## Usage

Follow these steps to get started with BBank:

1. **Sign Up**: Navigate to the signup page and create your account.
2. **Email Verification**: Check your email and click on the verification link sent to you.
3. **Log In**: Access your account using your login credentials.
4. **Account Verification**: Upload your FICA documents to verify your account.
5. **Start Transacting**: With your account set up, you can now begin depositing, withdrawing, and checking balances!

## API Endpoints

BBank's API provides a range of endpoints to cater to your banking needs:

### Authentication:

- **Obtain a JWT**:
    - Endpoint: `/api/auth/jwt/create/`
    - Method: POST
    - Required JSON Data: `{ "email": "your_email@example.com", "password": "your_password" }`

### Transactions:

- **Retrieve Transaction History**:
    - Endpoint: `/api/transaction-history/`
    - Method: GET

- **Create a New Transaction**:
    - Endpoint: `/api/create-transaction/`
    - Method: POST
    - Required JSON Data: `{ "amount": 100, "transaction_type": "deposit", "description":"Shoprite" }`

> **Note**: We're continually working to expand our API capabilities. Stay tuned for more endpoints and features in
> future releases!

