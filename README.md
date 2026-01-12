# Hybrid Blockchain Voting System

A decentralized e-voting prototype that addresses scalability and connectivity issues using a hybrid architecture.

## Features
* **Blockchain Security:** Uses Ethereum Smart Contracts (Ganache) for tamper-proof voting.
* **Hybrid Cloud:** Offloads audit logs to Supabase (PostgreSQL) for scalability.
* **Biometric Auth:** Integrates `face-api.js` for client-side face verification.
* **Offline Mode:** Supports vote queuing via LocalStorage when internet is lost.

## Tech Stack
* **Backend:** Python (Flask), Web3.py
* **Frontend:** HTML/JS, face-api.js
* **Blockchain:** Ganache (Local Ethereum)
* **Cloud:** Supabase

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run Ganache and update keys in `app.py`.
3. Deploy contract: `python deploy.py`
4. Start server: `python app.py`