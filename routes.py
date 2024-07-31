"""Routes for bank employee API.

NOTE: This module mocks a db using dictionaries: customer and accounts.

"""

from flask import request, jsonify
from util.generate import generate_uuid
import uuid

customers = {

        "195539a1-0f1e-4650-a60e-9e3d01aa40a2": {
            "accounts": [
                "94d40584-b585-43b6-b7ac-576918bcf492"
            ]
        },
        "8fe5d9ae-ff6c-4f47-bde9-f288ac502c4b": {
            "accounts": [
                "e335064d-d006-443c-b5d4-38a7c40f67e2"
            ]
        },
        "ac622822-e8ba-44c7-8f80-653beb16ac48": {
            "accounts": [
                "17e4544c-21e5-4194-8789-ba9386fe9b5f"
            ]
        }
}


accounts = { 
    "17e4544c-21e5-4194-8789-ba9386fe9b5f": {
            "balance": 3988,
            "transferHistory": [
                {
                    "amount": 401,
                    "transferToAccount": "94d40584-b585-43b6-b7ac-576918bcf492",
                    "transferType": "outbound"
                },
                {
                    "amount": 111,
                    "transferToAccount": "94d40584-b585-43b6-b7ac-576918bcf492",
                    "transferType": "outbound"
                }
            ]
        },
        "94d40584-b585-43b6-b7ac-576918bcf492": {
            "balance": 612,
            "transferHistory": [
                {
                    "amount": 401,
                    "otherAccount": "17e4544c-21e5-4194-8789-ba9386fe9b5f",
                    "transferType": "inbound"
                },
                {
                    "amount": 111,
                    "otherAccount": "17e4544c-21e5-4194-8789-ba9386fe9b5f",
                    "transferType": "inbound"
                }
            ]
        },
        "e335064d-d006-443c-b5d4-38a7c40f67e2": {
            "balance": 973,
            "transferHistory": []
        
    }
}


def register_routes(app):
    """
    Register routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """


    @app.route("/allCustomers", methods=["get"])
    def getAllCustomers():
        """
        Get all customers.

        Returns:
            Response: JSON response containing all customers and a 200 status code.
        """

        return jsonify({"allCustomers": customers}), 200
    
    @app.route("/allAccounts", methods=["get"])
    def getAllAccounts():
        """
        Get all accounts.

        Returns:
            Response: JSON response containing all accounts and a 200 status code.
        """

        return jsonify({"allAccounts": accounts}), 200
            
    @app.route("/createBankAccount", methods=["POST"])
    def createBankAccount():
        """
        Create a new bank account for an existing customer.

        The route assumes that a customer entry already exists and creates an account for that customer.

        Request Body:
            - customerId (str): The ID of the customer.
            - amount (float): The initial amount to deposit in the account. Must be 0 or greater.

        Returns:
            Response: JSON response with a success message and a 200 status code,
                      or an error message and a 400/404 status code if validation fails.
        """
        
        
        try:
            # Attempt to parse JSON data from the request body
            body = request.get_json()

            # Check if data is None or missing required fields
            if body is None:
                return jsonify({"error": "Invalid Body"}), 400
            
            intialAmount = body["amount"]
            # Attempt to convert the input to a float
            float_value = float(intialAmount)
            
            # Check if the float value is 0 or greater
            if float_value < 0:
                return jsonify({"error": "initial amount must not be negative"}), 400
            
            #validate that customer exists
            customerId = body["customerId"]
            if customerId not in customers:
                return jsonify({"error": "customer does not exist"}), 404
            
        except ValueError:
            # If conversion to float fails, return False
            return jsonify({"error": "amount must be a float type"}), 400
        
        
        # Add customer to customers.
        account_number = generate_uuid()

        customers[customerId]["accounts"].append(account_number)
        #add new account to accounts
        accounts[account_number] = {
            "balance": intialAmount,
            "transferHistory": [],
        }

        return jsonify({"message": f"created bank account with initial amount of {intialAmount}"}), 200

    @app.route("/transfer", methods=["PATCH"])
    def transfer():
        """
        Transfer an amount between two accounts.

        This route handles the transfer of a specified amount from one account to another.
        
        Request Body:
            - fromAccountId (str): The ID of the source account.
            - toAccountId (str): The ID of the destination account.
            - transferAmount (float): The amount to be transferred. Must be 0 or greater.
        
        Returns:
            Response: JSON response with a success message and a 200 status code,
                      or an error message and a 400/404 status code if validation fails.
        """


        try:
            # Attempt to parse JSON data from the request body
            body = request.get_json()

            # Check if data is None or missing required fields
            if body is None:
                return jsonify({"error": "Invalid Body"}), 400
            
            toAccountId = body["toAccountId"] 
            fromAccountId = body["fromAccountId"]
            if toAccountId not in accounts or fromAccountId not in accounts:
                return jsonify({"error": "one or both of the accounts do not exist"}), 404
            
            transferAmount = body["transferAmount"]
            # Attempt to convert the input to a float
            float_value = float(transferAmount)
            
            # Check if the float value is 0 or greater
            if float_value < 0:
                return jsonify({"error": "initial amount must not be negative"}), 400
            
            # Check if amount can be transfered (Account must not go below zero)
            if accounts[fromAccountId]["balance"] - transferAmount < 0:
                return jsonify({"error": "Transfer incomplete. Balance cannot be less than 0 after transfer."}), 400
            
            
        except ValueError:
            # If conversion to float fails, return False
            return jsonify({"error": "amount must be a float type"}), 400
        
        accounts[fromAccountId]["balance"]   -= transferAmount
        accounts[toAccountId]["balance"] += transferAmount
        accounts[fromAccountId]["transferHistory"].append({
            "transferType":"outbound",
            "amount":transferAmount,
            "transferToAccount":toAccountId
        })
        accounts[toAccountId]["transferHistory"].append({
            "transferType":"inbound",
            "amount":transferAmount,
            "otherAccount":fromAccountId
        })

        return  jsonify({"message": f"Transfer of amount {transferAmount} completed"}), 200

    @app.route("/getBalanceGivenAccount", methods=["GET"])
    def getBalanceGivenAccount():
        """
        Get the balance for a given account.

        Query Parameters:
            - accountId (str): The ID of the account.

        Returns:
            Response: JSON response containing the balance of the account and a 200 status code,
                  or an error message and a 404 status code if the account ID is invalid.
        """
        accountId = request.args.get('accountId')
        if accountId not in accounts:
            return jsonify({"error": "invalid accountId"}), 404
        
        balance = accounts[accountId]["balance"]
        return  jsonify({"balance": balance}), 200
    
    @app.route("/getAllAccountBalancesForCustomer", methods=["GET"])
    def getAllAccountBalancesForCustomer():
        """
        Get the balances of all accounts for a given customer.

        Query Parameters:
            - customerId (str): The ID of the customer.

        Returns:
            Response: JSON response containing the balances of all accounts for the customer and a 200 status code,
                    or an error message and a 404 status code if the customer ID is invalid.
        """
        customerId = request.args.get('customerId')
        if customerId not in customers:
            return jsonify({"error": "invalid customerId"}), 404
        accountsBalances = {}
        for account in customers[customerId]["accounts"]:
            accountsBalances[account] = accounts[account]["balance"]
        
        return  jsonify({"allBalances": accountsBalances}), 200
    

    @app.route("/transferHistory", methods=["GET"])
    def transferHistory():
        """
        Get the transfer history for a given account.

        Query Parameters:
            - accountId (str): The ID of the account.

        Returns:
            Response: JSON response containing the transfer history of the account and a 200 status code,
                    or an error message and a 404 status code if the account ID is invalid.
        """
        accountId = request.args.get('accountId')
        if accountId not in accounts:
            return jsonify({"error": "invalid accountId"}), 404
        
        history = accounts[accountId]["transferHistory"]
        return  jsonify({"transferHistory": history}), 200