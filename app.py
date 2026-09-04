from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
users = {
    1: {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob Smith", "email": "bob@example.com"},
}
next_id = 3


@app.route("/users", methods=["GET"])
def get_users():
    """Retrieve all users."""
    return jsonify(list(users.values())), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Retrieve a single user by ID."""
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""
    global next_id
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Missing required fields: 'name' and 'email'"}), 400

    new_user = {
        "id": next_id,
        "name": data["name"],
        "email": data["email"],
    }
    users[next_id] = new_user
    next_id += 1

    return jsonify(new_user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update an existing user's details."""
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])

    return jsonify(user), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user by ID."""
    user = users.pop(user_id, None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": f"User {user_id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)