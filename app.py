# ============================================================
# BloodLife - Blood Donation Website
# MySQL Database Version
# ============================================================

import os
import tempfile

import pymysql
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session, redirect


# ============================================================
# ENVIRONMENT
# ============================================================

# Loads .env locally.
# On Render, environment variables are provided directly.
load_dotenv()


# ============================================================
# APP SETUP
# ============================================================

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")


# ============================================================
# REQUIRED ENVIRONMENT VARIABLES
# ============================================================

required_vars = [
    "SECRET_KEY",
    "DB_HOST",
    "DB_USER",
    "DB_PASSWORD",
    "ADMIN_USER",
    "ADMIN_PASS",
]

missing_vars = [
    var for var in required_vars
    if not os.environ.get(var)
]

if missing_vars:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )


# ============================================================
# ADMIN CREDENTIALS
# ============================================================

ADMIN_USER = os.environ["ADMIN_USER"]
ADMIN_PASS = os.environ["ADMIN_PASS"]


# ============================================================
# AIVEN CA CERTIFICATE
# ============================================================

"""
Local development:
    DB_SSL_CA=C:\Users\MUSHFIQ\Downloads\ca.pem

Render:
    AIVEN_CA_CERT=<full certificate contents>

If AIVEN_CA_CERT exists, we create a temporary certificate
file and use it.

Otherwise, we use the local DB_SSL_CA path.
"""

AIVEN_CA_CERT = os.environ.get("AIVEN_CA_CERT")

if AIVEN_CA_CERT:
    # Render / Linux
    CA_FILE = os.path.join(
        tempfile.gettempdir(),
        "aiven-ca.pem"
    )

    with open(CA_FILE, "w", encoding="utf-8") as f:
        f.write(AIVEN_CA_CERT)

else:
    # Local development
    CA_FILE = os.environ.get("DB_SSL_CA")


if not CA_FILE or not os.path.exists(CA_FILE):
    raise RuntimeError(
        "Aiven CA certificate is not configured correctly. "
        "Set AIVEN_CA_CERT on Render or DB_SSL_CA locally."
    )


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ.get("DB_NAME", "blood_donation"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "ssl": {
        "ca": CA_FILE
    }
}


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db():
    return pymysql.connect(**DB_CONFIG)


# ============================================================
# PAGE ROUTES
# ============================================================

@app.route("/")
def home():
    return redirect("/donors")


@app.route("/donors")
def donors_page():
    return render_template("donors.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("logged_in"):
        return redirect("/admin")

    return render_template("dashboard.html")


# ============================================================
# API ROUTES
# ============================================================

# ------------------------------------------------------------
# GET DATABASE STATISTICS
# ------------------------------------------------------------

@app.route("/api/stats")
def api_stats():

    conn = get_db()

    try:
        with conn.cursor() as cur:

            # Total donors and available donors
            cur.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    SUM(is_available) AS available
                FROM donors
                """
            )

            row = cur.fetchone()

            # Blood group counts
            cur.execute(
                """
                SELECT
                    blood_group,
                    COUNT(*) AS count
                FROM donors
                GROUP BY blood_group
                """
            )

            blood_counts = {
                r["blood_group"]: r["count"]
                for r in cur.fetchall()
            }

            # Locations
            cur.execute(
                """
                SELECT DISTINCT location
                FROM donors
                WHERE location IS NOT NULL
                AND location != ''
                """
            )

            locations = [
                r["location"]
                for r in cur.fetchall()
            ]

        return jsonify({
            "total": row["total"] or 0,
            "available": int(row["available"] or 0),
            "locations": locations,
            "blood_counts": blood_counts
        })

    finally:
        conn.close()


# ------------------------------------------------------------
# GET DONORS
# ------------------------------------------------------------

@app.route("/api/donors")
def api_donors():

    search = request.args.get(
        "search",
        ""
    ).lower()

    blood = request.args.get(
        "blood",
        ""
    )

    location = request.args.get(
        "location",
        ""
    ).lower()

    conn = get_db()

    try:
        with conn.cursor() as cur:

            query = """
                SELECT *
                FROM donors
                WHERE 1=1
            """

            params = []

            # Blood group filter
            if blood:
                query += """
                    AND blood_group = %s
                """

                params.append(blood)

            # Location filter
            if location:
                query += """
                    AND LOWER(location) LIKE %s
                """

                params.append(
                    f"%{location}%"
                )

            # General search
            if search:
                query += """
                    AND (
                        LOWER(name) LIKE %s
                        OR LOWER(location) LIKE %s
                        OR phone LIKE %s
                    )
                """

                params.extend([
                    f"%{search}%",
                    f"%{search}%",
                    f"%{search}%"
                ])

            query += """
                ORDER BY id DESC
            """

            cur.execute(
                query,
                params
            )

            return jsonify(
                cur.fetchall()
            )

    finally:
        conn.close()


# ------------------------------------------------------------
# ADD DONOR
# ------------------------------------------------------------

@app.route(
    "/api/donors",
    methods=["POST"]
)
def api_add_donor():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request data"
        }), 400

    # Required fields
    if (
        not data.get("name")
        or not data.get("blood_group")
        or not data.get("phone")
        or not data.get("location")
    ):
        return jsonify({
            "error": (
                "Name, blood group, phone, "
                "and location are required"
            )
        }), 400

    conn = get_db()

    try:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO donors (
                    name,
                    blood_group,
                    phone,
                    email,
                    location,
                    address,
                    message,
                    age,
                    gender
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    data["name"],
                    data["blood_group"],
                    data["phone"],
                    data.get("email", ""),
                    data["location"],
                    data.get("address", ""),
                    data.get("message", ""),
                    data.get("age"),
                    data.get("gender", "")
                )
            )

            conn.commit()

            donor_id = cur.lastrowid

        return jsonify({
            "message": "Donor registered successfully!",
            "id": donor_id
        }), 201

    finally:
        conn.close()


# ------------------------------------------------------------
# DELETE DONOR
# ------------------------------------------------------------

@app.route(
    "/api/donors/<int:donor_id>",
    methods=["DELETE"]
)
def api_delete_donor(donor_id):

    if not session.get("logged_in"):
        return jsonify({
            "error": "Not logged in"
        }), 401

    conn = get_db()

    try:
        with conn.cursor() as cur:

            cur.execute(
                """
                DELETE FROM donors
                WHERE id = %s
                """,
                (donor_id,)
            )

            conn.commit()

        return jsonify({
            "message": "Donor deleted"
        })

    finally:
        conn.close()


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route(
    "/api/login",
    methods=["POST"]
)
def api_login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request data"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if (
        username == ADMIN_USER
        and password == ADMIN_PASS
    ):
        session["logged_in"] = True

        return jsonify({
            "message": "Login successful"
        })

    return jsonify({
        "error": "Invalid username or password"
    }), 401


# ============================================================
# ADMIN LOGOUT
# ============================================================

@app.route(
    "/api/logout",
    methods=["POST"]
)
def api_logout():

    session.clear()

    return jsonify({
        "message": "Logged out"
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 50)

    print(
        "  BloodLife - MySQL Database Version"
    )

    print(
        "  Open: http://localhost:5000"
    )

    print(
        "  Admin: http://localhost:5000/admin"
    )

    print("=" * 50 + "\n")

    app.run(
        debug=True,
        port=5000
    )