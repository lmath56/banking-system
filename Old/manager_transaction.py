# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Manager for Transaction Class - Version 1


def add_transaction(transaction_id, transaction_type, amount, timestamp, description, account_number, recipient_account_number):
    from api import session, Transaction
    new_transaction = Transaction(transaction_id, transaction_type, amount, timestamp, description, account_number, recipient_account_number)
    session.add(new_transaction)
    session.commit()
    return new_transaction

def delete_transaction(transaction_id:int):
    DELETE_TRANSACTION = "DELETE FROM transaction WHERE transaction_id=?"
    from api import session, Transaction
    for transaction in session.query(Transaction).all():
        if transaction.transaction_id == transaction_id:
            input(f"Are you sure you would like permanenty delete transaction ID: {transaction_id}? WARNING: This action can not be reversed. (Y/N) ") 
            if input == "Y"or input == "y":
                session.execute(DELETE_TRANSACTION, (transaction_id))
                print(f"Transaction ID: {transaction_id} has been removed.")
            else:
                return f"Transaction ID: {transaction_id} has NOT been removed."
            return
    return f"Transaction ID: {transaction_id} is not found."