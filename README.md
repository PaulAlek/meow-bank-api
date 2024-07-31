# meow-bank-api

This is a simple Flask application that provides various endpoints to manage customers and their accounts, including functionalities for creating bank accounts, transferring amounts, and retrieving balances and transfer histories.

### Prerequisites

-   Python 3.6 or higher
-   pip (Python package installer)

### Setting Up the Project

1. **Clone the repository**:

    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name

Create a virtual environment:

python -m venv venv
Activate the virtual environment:

On macOS/Linux:

source venv/bin/activate
On Windows:

.\venv\Scripts\activate
Install the dependencies:

pip install -r requirements.txt

### Usage

Running the Flask Application
Ensure the virtual environment is activated:

source venv/bin/activate # On macOS/Linux
.\venv\Scripts\activate # On Windows
Run the application:

python app.py
Access the application:

Consider using Postman or CURL.

Base URL
http://127.0.0.1:8000.

Endpoints
/allCustomers (GET)
Retrieve a list of all customers.

/allAccounts (GET)
Retrieve a list of all accounts.

/createBankAccount (POST)
Create a new bank account for an existing customer.

Request Body:

json
Copy code
{
"customerId": "string",
"amount": "float"
}

Responses:

200 OK: Successfully created the bank account.
400 Bad Request: Invalid input.
404 Not Found: Customer does not exist.
/transfer (PATCH)
Transfer an amount between two accounts.

Request Body:

json
Copy code
{
"fromAccountId": "string",
"toAccountId": "string",
"transferAmount": "float"
}
Responses:

200 OK: Successfully completed the transfer.
400 Bad Request: Invalid input or insufficient funds.
404 Not Found: One or both accounts do not exist.
/getBalanceGivenAccount (GET)
Retrieve the balance for a given account.

Query Parameters:

accountId: The ID of the account.
Responses:

200 OK: Successfully retrieved the balance.
404 Not Found: Invalid account ID.
/getAllAccountBalancesForCustomer (GET)
Retrieve the balances of all accounts for a given customer.

Query Parameters:

customerId: The ID of the customer.
Responses:

200 OK: Successfully retrieved all balances.
404 Not Found: Invalid customer ID.

/transferHistory (GET)
Retrieve the transfer history for a given account.

Query Parameters:

accountId: The ID of the account.
Responses:

200 OK: Successfully retrieved the transfer history.
404 Not Found: Invalid account ID.
