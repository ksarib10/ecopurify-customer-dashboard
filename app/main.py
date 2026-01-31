from flask import Flask, redirect, request, jsonify, render_template, session

from auth_service import authenticate_customer
from sheets import (
    find_plants_by_customer,
    get_sheet,
    update_health_by_row
)
from utils import days_since, health_from_days


# -------------------------
# App Setup
# -------------------------

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
app.secret_key = "ecopurify-secret-key"


# -------------------------
# Authentication
# -------------------------

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request payload"
        }), 400

    customer_id = data.get("customer_id")
    password = data.get("password")

    if not customer_id or not password:
        return jsonify({
            "success": False,
            "message": "Customer ID and password required"
        }), 400

    plants, error = authenticate_customer(customer_id, password)

    if error:
        return jsonify({"success": False, "message": error}), 401

    if not plants:
        return jsonify({"success": False, "message": "No plants found"}), 401

    session.clear()
    session["customer_id"] = customer_id
    session["plants"] = plants
    session["active_plant_id"] = plants[0]["plant_id"]

    return jsonify({"success": True}), 200


# -------------------------
# Plant Selection
# -------------------------

@app.route("/set-active-plant", methods=["POST"])
def set_active_plant():
    data = request.get_json()
    plant_id = data.get("plant_id")

    if not plant_id:
        return {"success": False}, 400

    session["active_plant_id"] = plant_id
    return {"success": True}


# -------------------------
# Pages
# -------------------------

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "customer_id" not in session or "plants" not in session:
        return redirect("/")

    plants = session["plants"]
    active_id = session.get("active_plant_id")

    active_plant = next(
        (p for p in plants if p["plant_id"] == active_id),
        plants[0]
    )

    # Compute service age
    last_service = active_plant.get("last_service_date")
    days_passed = days_since(last_service) if last_service else 0

    return render_template(
        "dashboard.html",
        plant=active_plant,
        plants=plants,
        customer_name=active_plant["customer_name"],
        days_passed=days_passed
    )


# -------------------------
# Refresh Logic
# -------------------------

@app.route("/refresh")
def refresh():
    if "customer_id" not in session:
        return redirect("/")

    customer_id = session["customer_id"]
    active_plant_id = session.get("active_plant_id")

    sheet = get_sheet()
    records = sheet.get_all_records()

    # Update health values in sheet
    for idx, row in enumerate(records, start=2):
        if row.get("customer_id") != customer_id:
            continue

        last_service = row.get("last_service_date")
        days = days_since(last_service) if last_service else 0
        new_health = health_from_days(days)

        updates = {
            "health_pp": new_health,
            "health_cto": new_health,
            "health_ro": new_health,
            "health_mineralization": new_health,
        }

        update_health_by_row(idx, updates)

    # Reload plants from sheet
    fresh_plants = find_plants_by_customer(customer_id)

    for plant in fresh_plants:
        plant.pop("password", None)

    session["plants"] = fresh_plants

    # Preserve active plant
    if not any(p["plant_id"] == active_plant_id for p in fresh_plants):
        session["active_plant_id"] = fresh_plants[0]["plant_id"]

    return redirect("/dashboard")


# -------------------------
# Logout
# -------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
