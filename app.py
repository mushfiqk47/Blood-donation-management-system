import pymysql
from flask import Flask, render_template, request, jsonify, session, redirect

app = Flask(__name__)
app.secret_key = 'bloodlife-secret-key-2026'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'blood_donation',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'


def get_db():
    return pymysql.connect(**DB_CONFIG)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/donors')
def donors_page():
    return render_template('donors.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/donor/<int:donor_id>')
def donor_detail_page(donor_id):
    return render_template('donor_detail.html', donor_id=donor_id)

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect('/admin')
    return render_template('dashboard.html')


@app.route('/api/stats')
def api_stats():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as total FROM donors")
            total = cur.fetchone()['total'] or 0

            cur.execute("SELECT blood_group, COUNT(*) as count FROM donors GROUP BY blood_group")
            blood_counts = {r['blood_group']: r['count'] for r in cur.fetchall()}

            cur.execute("SELECT DISTINCT location FROM donors")
            locations = [r['location'] for r in cur.fetchall()]

        return jsonify({'total': total, 'available': total, 'locations': locations, 'blood_counts': blood_counts})
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

@app.route('/api/donors/<int:donor_id>')
def api_donor(donor_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM donors WHERE id = %s", (donor_id,))
            donor = cur.fetchone()
            if donor:
                return jsonify(donor)
            return jsonify({'error': 'Donor not found'}), 404
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
                "INSERT INTO donors (name, blood_group, phone, email, location, message, age, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (data['name'], data['blood_group'], data['phone'],
                 data.get('email', ''), data['location'],
                 data.get('message', ''), data.get('age'), data.get('gender', ''))
            )
            conn.commit()
        return jsonify({'message': 'Donor registered successfully!', 'id': cur.lastrowid}), 201
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


if __name__ == '__main__':
    print("\n  BloodLife - http://localhost:5000")
    print("  Admin: http://localhost:5000/admin (admin / admin123)\n")
    app.run(debug=True, port=5000)
