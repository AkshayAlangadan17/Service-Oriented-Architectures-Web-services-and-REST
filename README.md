# Distributed Systems – Assignment 2
**Service-Oriented Architecture with Python + Flask**
# Akshay Alangadan, Faisal Khan, Heshan Ryan Raj
---

##  Overview

This assignment implements a minimal two-service architecture:

- `auth_service.py`: Handles user authentication and role-based access via token issuance.
- `transaction.py`: Handles transaction storage and fraud result access, protected by user roles.

Everything is built using **Flask**, and all communication is done via **REST APIs**.

---

## Setup Instructions

### 1. Requirements

Install dependencies:

```bash
pip install flask requests
```

### 2. Folder Contents

- `auth_service.py`: Login + token generation + token verification (in-memory)
- `transaction.py`: Transaction + fraud result management (with SQLite)
- `transactions.db`: Auto-generated SQLite DB with `transactions` and `results`
- `auth_service.log`: Log of all requests to the auth service
- `transaction_service.log`: Log of all requests to the transaction service
- `README.md`: This file

---

##  How to Run

### Step 1: Start Both Services in Two Terminals

> Open two terminal windows (or two tabs in VSCode):

#### Terminal 1 – Run the Auth Service

```bash
python auth_service.py  # → http://localhost:5000 
```

Expected output:
```
* Serving Flask app 'auth_service'
 * Debug mode: off

```

#### Terminal 2 – Run the Transaction Service

```bash
python transaction.py # → http://localhost:5001
```
```

Expected output:
```
 * Serving Flask app 'transaction'
 * Debug mode: off
```

---

## How to Use (with Postman or curl)

### Step 2: Login (Get a Token)

**POST** `http://localhost:5000/auth/login`

**Body (JSON):**

```json
{
  "username": "admin",
  "password": "adminpass"
}
```

Copy the `token` from the response.

| Username  | Password      | Role          |
|-----------|---------------|---------------|
| admin     | adminpass     | Administrator |
| agent     | agentpass     | Agent         |
| secretary | secretarypass | Secretary     |

---

### Step 3: Add a Transaction

**POST** `http://localhost:5001/transactions`  
**Headers**:
- `Authorization: <your token>`
- `Content-Type: application/json`

**Body:**

```json
{
  "customer": "cust1",
  "status": "submitted",
  "vendor_id": "v123",
  "amount": 99.9
}
```

Expected Response:

```json
{ "success": "Transaction added" }
```

---

### Step 4: Update a Transaction

**PUT** `http://localhost:5001/transactions/1`  
(Same headers)

**Body:**

```json
{
  "status": "accepted"
}
```

Expected Response:

```json
{ "success": "Transaction updated" }
```

---

### Step 5: Check Fraud Result

**GET** `http://localhost:5001/results/1`  
(Same Authorization header)

Expected Response:

```json
{ "error": "Result not found" }
```

(Until a result is inserted into the DB)

---

## Access Control Summary

| Role        | Can Login | Add/Update Transactions | Get Results |
|-------------|-----------|-------------------------|-------------|
| Administrator | ✅       | ✅                      | ✅           |
| Agent         | ✅       | ✅                      | ✅           |
| Secretary     | ✅       | ❌ (403)                | ❌ (403)     |

---

## How to Use These APIs with Postman

1. **Open Postman** and create a new `POST` request:
   - URL: `http://localhost:5000/auth/login`
   - Set **Body** to `raw` and choose **JSON**
   - Paste:
     ```json
     {
       "username": "admin",
       "password": "adminpass"
     }
     ```

2. **Click Send** and copy the `token` from the response.

3. Use that token in the **Authorization header** for future requests:
   - Key: `Authorization`
   - Value: `<your token here>`

4. Set `Content-Type` header to `application/json` for all request bodies.

This will allow you to test login, transaction creation, updating, and result lookup with ease.

---

## Notes 

- No persistent user database is used — everything is in-memory in `auth_service.py`
- SQLite is auto-created (`transactions.db`)
- Full request/response logging is enabled in `.log` files
- Services can be tested using Postman or curl
- Code is modular and clearly separated by role/responsibility

---

## Tech Stack

- Python 3
- Flask (micro web framework)
- SQLite (built-in)
- Postman / curl for testing

---
