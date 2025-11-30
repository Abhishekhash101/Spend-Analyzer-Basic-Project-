# Spend Analyser from SMS

This project takes SMS messages from your phone and automatically extracts financial transactions such as debits and credits. It then provides a visual breakdown of spending and income, grouped by merchant and by bank account.

The app supports both SMS backups in XML format and pre-processed CSV files. When SMS data is uploaded, the app filters out non-financial messages and extracts transaction-related ones by identifying banking/UPI keywords. Each extracted SMS is transformed into a structured transaction row containing:

- date  
- raw SMS message  
- amount  
- txn_type (debit or credit)  
- merchant name (parsed from message)  
- account_id (inferred from SMS sender or account digits)

The app displays:
- total debits (money spent)
- total credits (money received)
- debit ranking by merchant name
- credit ranking by merchant name
- debit per bank account
- credit per bank account

This project is a part of my basic data science learning work, focusing on data extraction, text processing, and financial pattern visualization from real-world SMS data.
