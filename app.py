# ============================================================
# BloodLife - Blood Donation Website (MySQL Database Version)
# ============================================================

import os

import pymysql
from flask import Flask, render_template, request, jsonify, session, redirect

# --- App Setup ---
app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

required_db_vars = [
    "DB_HOST",
    "DB_USER",
    "DB_PASSWORD"
]

missing_vars = [var for var in required_db_vars if not os.environ.get(var)]

if missing_vars:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

# --- Database Configuration ---
DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME", "blood_donation"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "ssl": {
        "ca": os.environ.get("DB_SSL_CA")
    }
}

# --- Admin Credentials (from database) ---
ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'


def get_db():
    return pymysql.connect(**DB_CONFIG)


# =====================
# PAGE ROUTES (HTML)
# =====================

@app.route('/')
def home():
    return redirect('/donors')

@app.route('/donors')
def donors_page():
    return render_template('donors.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect('/admin')
    return render_template('dashboard.html')

# =====================
# API ROUTES (JSON)
# =====================

@app.route('/api/stats')
def api_stats():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as total, SUM(is_available) as available FROM donors")
            row = cur.fetchone()

            cur.execute("SELECT blood_group, COUNT(*) as count FROM donors GROUP BY blood_group")
            blood_counts = {r['blood_group']: r['count'] for r in cur.fetchall()}

            cur.execute("SELECT DISTINCT location FROM donors")
            locations = [r['location'] for r in cur.fetchall()]

        return jsonify({
            'total': row['total'] or 0,
            'available': int(row['available'] or 0),
            'locations': locations,
            'blood_counts': blood_counts
        })
    finally:
        conn.close()

@app.route('/api/donors')
def api_donors():
    search = request.args.get('search', '').lower()
    blood = request.args.get('blood', '')
    location = request.args.get('location', '').lower()

    conn = get_db()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM donors WHERE 1=1"
            params = []

            if blood:
                query += " AND blood_group = %s"
                params.append(blood)
            if location:
                query += " AND LOWER(location) LIKE %s"
                params.append(f'%{location}%')
            if search:
                query += " AND (LOWER(name) LIKE %s OR LOWER(location) LIKE %s OR phone LIKE %s)"
                params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])

            query += " ORDER BY id DESC"
            cur.execute(query, params)
            return jsonify(cur.fetchall())
    finally:
        conn.close()

@app.route('/api/donors', methods=['POST'])
def api_add_donor():
    data = request.get_json()

    if not data.get('name') or not data.get('blood_group') or not data.get('phone') or not data.get('location'):
        return jsonify({'error': 'Name, blood group, phone, and location are required'}), 400

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO donors (name, blood_group, phone, email, location, address, message, age, gender)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    data['name'],
                    data['blood_group'],
                    data['phone'],
                    data.get('email', ''),
                    data['location'],
                    data.get('address', ''),
                    data.get('message', ''),
                    data.get('age'),
                    data.get('gender', '')
                )
            )
            conn.commit()
            donor_id = cur.lastrowid
        return jsonify({'message': 'Donor registered successfully!', 'id': donor_id}), 201
    finally:
        conn.close()

@app.route('/api/donors/<int:donor_id>', methods=['DELETE'])
def api_delete_donor(donor_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM donors WHERE id = %s", (donor_id,))
            conn.commit()
        return jsonify({'message': 'Donor deleted'})
    finally:
        conn.close()

# =====================
# ADMIN LOGIN/LOGOUT
# =====================

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if data.get('username') == ADMIN_USER and data.get('password') == ADMIN_PASS:
        session['logged_in'] = True
        return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'message': 'Logged out'})

# =====================
# RUN
# =====================

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  BloodLife - MySQL Database Version")
    print("  Open: http://localhost:5000")
    print("  Admin: http://localhost:5000/admin")
    print("  Username: admin | Password: admin123")
    print("=" * 50 + "\n")
    app.run(debug=True, port=5000)
