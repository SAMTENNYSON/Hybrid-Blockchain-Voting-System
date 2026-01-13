from supabase import create_client, Client
import datetime

# --- CONFIGURATION ---
SUPABASE_URL = "YOUR_SUPABASE_URL_HERE"
SUPABASE_KEY = "YOUR_SUPABASE_KEY_HERE"

print("1. Connecting to Supabase...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("2. Attempting to insert test row...")
    
    # FIX: We now send the current time manually
    current_time = datetime.datetime.now().isoformat()
    
    data = {
        "created_at": current_time,
        "voter_hash": "TEST_USER_123", 
        "candidate_id": 99, 
        "status": "Cloud Test Successful"
    }
    
    response = supabase.table("audit_logs").insert(data).execute()
    
    print("✅ SUCCESS! Check your Supabase Dashboard now.")
    print("Response:", response)

except Exception as e:
    print("\n❌ FAILURE:", e)