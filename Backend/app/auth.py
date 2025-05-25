# from config import test_mongo_connection
# test_mongo_connection()
from flask import Blueprint, request, jsonify
from .extensions import bcrypt, mongo
from .db_utils import get_db_collection
from .config import Config
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId

auth_bp = Blueprint('auth', __name__)

auth_collection = get_db_collection(Config.AUTH_DB, Config.AUTH_COLLECTION)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if auth_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400
    
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    auth_collection.insert_one({
        "email": email,
        "password": hashed_pw,
        "username": username
    })
    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = auth_collection.find_one({"email": email})
    if user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid email or password"}), 401
    
    token = create_access_token(identity=str(user['_id']))
    return jsonify({"access_token": token}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = auth_collection.find_one({"_id": ObjectId(user_id)})
    return jsonify({
        "email": user['email'],
        "username": user['username']
    }), 200