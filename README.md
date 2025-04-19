# 📦 DistributedSystems – Assignment 2

A super‑simple two‑service demo (Python + Flask)

---

##  What’s inside?

| File | Purpose |
| ---- | ------- |
| **auth_service.py** | Issues & verifies Base64 tokens (in‑memory). |
| **transaction_service.py** | Admins & Agents add / update transactions and query fraud‑results (SQLite). |
| **transactions.db** | SQLite file (auto‑created). |
| **auth_service.log / transaction_service.log** | Per‑service request/response logs. |

---\_service.py**                      | Admins & Agents add / update transactions and query fraud‑results (SQLite). |
| **transactions.db**                              | SQLite file (auto‑created).                                                 |
| **auth\_service.log / transaction\_service.log** | Per‑service request/response logs.                                          |

---

## 🚀 Run it (two terminals)

```bash
# Terminal 1 – Authentication Service
python auth_service.py    # → http://localhost:5000

# Terminal 2 – Transaction Service
python transaction_service.py   # → http://localhost:5001
```

> Requires only `pip install flask requests` inside your virtual‑env.

---

## 🔐 Step 1 – Login (get a token)

`POST  http://localhost:5000/auth/login`

```json
{ "username": "admin", "password": "adminpass" }
```

Copy the `token` value from the JSON response.

| username  | password      | role          |
| --------- | ------------- | ------------- |
| admin     | adminpass     | Administrator |
| agent     | agentpass     | Agent         |
| secretary | secretarypass | Secretary     |

---

## 💳 Step 2 – Add a transaction

`POST  http://localhost:5001/transactions`

```http
Header  Authorization: <your‑token>
Header  Content‑Type:  application/json
```

```json
{
  "customer":   "cust1",
  "status":     "submitted",
  "vendor_id":  "v123",
  "amount":      99.9
}
```

Expected response:

```json
{ "success": "Transaction added" }
```

\###Update status

```http
PUT /transactions/1   (same headers)
Body: { "status": "accepted" }
```

\###Check result (example)

```http
GET /results/1   (same Authorization header)
```

Will reply *Result not found* until an ML result row is inserted.

---

##  How it works – one paragraph

*auth\_service.py* keeps a small user table in memory and returns random Base64 tokens. *transaction\_service.py* calls `/auth/verify` on every request and allows only **Administrator** & **Agent** roles. Each request/response is logged. Transaction data and fraud‑results live in a single SQLite DB, so there’s nothing to configure.

---


