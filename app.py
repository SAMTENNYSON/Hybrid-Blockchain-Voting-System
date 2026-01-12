from flask import Flask, render_template, request, jsonify
from web3 import Web3
from supabase import create_client, Client # Import Cloud Library
import json
import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
# 1. Blockchain Config
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))
my_address = "YOUR_GANACHE_ADDRESS_HERE" 
private_key = "YOUR_PRIVATE_KEY_HERE"

# 2. Cloud Config (Supabase)
SUPABASE_URL = "YOUR_SUPABASE_URL_HERE"
SUPABASE_KEY = "YOUR_SUPABASE_KEY_HERE"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load Contract
with open("contract_data.json", "r") as file:
    data = json.load(file)
    contract = w3.eth.contract(address=data["contract_address"], abi=data["abi"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_candidates", methods=["GET"])
def get_candidates():
    count = contract.functions.candidatesCount().call()
    candidates_list = []
    for i in range(1, count + 1):
        candidate = contract.functions.candidates(i).call()
        candidates_list.append({"id": candidate[0], "name": candidate[1], "voteCount": candidate[2]})
    return jsonify(candidates_list)

@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    c_id = int(data["id"])
    v_addr = data.get("voter_address", "anon")

    try:
        # A. BLOCKCHAIN TRANSACTION (The Secure Vote)
        nonce = w3.eth.get_transaction_count(my_address)
        txn = contract.functions.vote(c_id).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'from': my_address
        })
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)
        receipt = w3.to_hex(tx_hash)

        # B. CLOUD LOGGING (The "Hybrid" Part)
        # We save a record to Supabase Cloud for analytics
        try:
            log_entry = {
                "created_at": datetime.datetime.now().isoformat(),
                "voter_hash": v_addr, 
                "candidate_id": c_id, 
                "status": "Confirmed On-Chain"
            }
            supabase.table("audit_logs").insert(log_entry).execute()
            print("✅ Log sent to Cloud (Supabase)")
        except Exception as cloud_error:
            print(f"⚠️ Cloud Log Failed (Vote still counted): {cloud_error}")

        return jsonify({"message": "Success", "hash": receipt}), 200

    except Exception as e:
        # Log failure to Cloud too
        try:
            supabase.table("audit_logs").insert({
                "voter_hash": v_addr, 
                "candidate_id": c_id, 
                "status": f"Failed: {str(e)}"
            }).execute()
        except:
            pass
            
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)