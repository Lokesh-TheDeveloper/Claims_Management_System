from sqlalchemy import create_engine
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

engine = create_engine("mysql+pymysql://flaskuser:new_password@localhost:3306/claims_db")


app = Flask(__name__)

# Configure MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:new_password@localhost/claims_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Policyholder(db.Model):
    __tablename__ = 'policyholders'
    holder_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Policy(db.Model):
    __tablename__ = 'policies'
    policy_id = db.Column(db.Integer, primary_key=True)
    policyholder_id = db.Column(db.Integer, db.ForeignKey('policyholders.holder_id'))
    coverage_amount = db.Column(db.Float, nullable=False)

class Claim(db.Model):
    __tablename__ = 'claims'
    claim_id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.policy_id'))
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')

# API Routes

# ➤ Create a Claim
@app.route('/claim', methods=['POST'])
def create_claim():
    data = request.json
    policy = Policy.query.get(data['policy_id'])
    if not policy:
        return jsonify({"error": "Invalid policy ID"}), 400
    if data['amount'] > policy.coverage_amount:
        return jsonify({"error": "Claim exceeds policy limit"}), 400

    new_claim = Claim(policy_id=data['policy_id'], amount=data['amount'])
    db.session.add(new_claim)
    db.session.commit()
    return jsonify({"message": "Claim created successfully!"})

# ➤ Get Claim by ID
@app.route('/claim/<int:claim_id>', methods=['GET'])
def get_claim(claim_id):
    claim = Claim.query.get(claim_id)
    return jsonify(vars(claim)) if claim else jsonify({"error": "Claim not found"}), 404

# Initialize Database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


