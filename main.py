# policy with coverage amount 
class Policy:
    def __init__(self, policy_id, policyholder, coverage_amount):
        self.policy_id = policy_id
        self.policyholder = policyholder
        self.coverage_amount = coverage_amount



class Policyholder:
    def __init__(self, holder_id, name):
        self.holder_id = holder_id
        self.name = name

class Claim:
    def __init__(self, claim_id, policy_id, amount, status="Pending"):
        self.claim_id = claim_id
        self.policy_id = policy_id
        self.amount = amount
        self.status = status


# CRUD FUCNTIONS FOR POLICYHOLDER
class ClaimsManager:
    def __init__(self):
        self.claims = {}  # Stores claims in memory

    def create_claim(self, claim_id, policy_id, amount, policy):
        if amount > policy.coverage_amount:
            return "Claim amount exceeds policy coverage!"
        self.claims[claim_id] = Claim(claim_id, policy_id, amount)
        return f"Claim {claim_id} created!"

    def get_claim(self, claim_id):
        return self.claims.get(claim_id, "Claim not found")

    def update_claim(self, claim_id, new_status):
        if claim_id in self.claims:
            self.claims[claim_id].status = new_status
            return f"Claim {claim_id} updated!"
        return "Claim not found"

    def delete_claim(self, claim_id):
        return self.claims.pop(claim_id, "Claim not found")




def validate_claim(claim_id, amount, policy, claims_manager):
    if claim_id in claims_manager.claims:
        return "Claim ID already exists!"
    if amount > policy.coverage_amount:
        return "Claim amount exceeds policy limit!"
    return None




# API Creation

from flask import Flask, request, jsonify

app = Flask(__name__)     # Initializes a Flask application instance named app.


# Now we need something to store data 



claims_manager = ClaimsManager()

@app.route("/claim", methods=["POST"])     # This registers an endpoint (/claim) that listens for POST requests to create a new claim.
def create_claim():                        #Defines the function that handles the POST request for creating claims
    data = request.json
    policy = Policy(data["policy_id"], "John Doe", 10000)  # Example policy
    validation_error = validate_claim(data["claim_id"], data["amount"], policy, claims_manager)
    
    if validation_error:
        return jsonify({"error": validation_error}), 400    # 400 htp bad response code

    response = claims_manager.create_claim(data["claim_id"], data["policy_id"], data["amount"], policy)   #Calls create_claim() from ClaimsManager to store the claim in memory.
    return jsonify({"message": response})


@app.route("/claim/<claim_id>", methods=["GET"])
def get_claim(claim_id):
    claim = claims_manager.get_claim(int(claim_id))
    return jsonify({"claim": vars(claim) if claim != "Claim not found" else claim})

if __name__ == "__main__":  #ensures the script runs only when executed directly (not when imported as a module).
    app.run(debug=True)   #Auto-reloading on code changes.


