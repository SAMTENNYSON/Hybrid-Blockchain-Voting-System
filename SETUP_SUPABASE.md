# ☁️ Supabase Cloud Setup Guide

This project uses **Supabase** (an open-source Firebase alternative) to store audit logs and analytics off-chain. This hybrid approach ensures the system remains scalable while keeping votes secure on the Blockchain.

Follow these steps to configure the cloud database.

## 1. Create a Project
1. Go to [Supabase.com](https://supabase.com/) and sign in.
2. Click **"New Project"**.
3. Enter the following details:
   - **Name:** `Voting_Audit_Logs`
   - **Database Password:** (Create a strong password and save it)
   - **Region:** Choose a region closest to you (e.g., Mumbai, Singapore).
4. Click **"Create new project"** and wait ~1 minute for the database to provision.

## 2. Create the Table (`audit_logs`)
We need a table to store the logs when someone votes.

1. On the left sidebar, click the **Table Editor** icon (looks like a grid/table).
2. Click **"New Table"**.
3. **Name:** `audit_logs`
4. **Uncheck** "Enable Row Level Security (RLS)" (See Step 3 for details).
5. **Columns:** Add the following columns:

| Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `id` | `int8` | *Auto-generated* | Primary Key |
| `created_at` | `timestamptz` | `now()` | Timestamp of the log |
| `voter_hash` | `text` | *NULL* | Anonymized voter ID |
| `candidate_id` | `int8` | *NULL* | ID of the candidate voted for |
| `status` | `text` | *NULL* | Status message (e.g., "Confirmed") |

6. Click **Save**.

## 3. Disable RLS (Important for Demo)
By default, Supabase blocks anonymous writes. Since our Python script connects as an "Anonymous" client, we must disable Row Level Security (RLS) for this table.

1. If you didn't uncheck it during creation, go to the **Table Editor**.
2. Select `audit_logs`.
3. Look for the **"RLS"** badge in the top-right corner.
4. Click it and select **"Disable RLS"**.
5. Confirm the warning.

> **Note:** In a real production environment, you would keep RLS enabled and use secure Service Role keys. We disable it here for simplicity in the Proof of Concept.

## 4. Get Connection Keys
To connect your Python Flask app to this database, you need the API credentials.

1. Go to **Project Settings** (Gear icon at the bottom left).
2. Select **API**.
3. Copy these two values:
   - **Project URL:** (e.g., `https://xyz.supabase.co`)
   - **anon public key:** (The long string starting with `ey...`)

## 5. Update Python Configuration
Paste these keys into your `app.py` or `test_cloud.py` file:

```python
SUPABASE_URL = "[https://your-project-id.supabase.co](https://your-project-id.supabase.co)"
SUPABASE_KEY = "your-anon-key-here"