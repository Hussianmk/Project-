from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json, os, uuid
from datetime import datetime, date
from functools import wraps

app = Flask(__name__)
app.secret_key = 'ncc_army_wing_secret_2024'

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# ─────────────────────────────────────────────────────────────────────────────
# DATA HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def load_data():
    if not os.path.exists(DATA_FILE):
        return init_default_data()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def init_default_data():
    data = {
        "users": [
            {"id": "u1", "username": "ano_sharma",  "password": "ano123",  "role": "ANO",    "name": "Lt. Rajiv Sharma",   "email": "sharma@ncc.in",  "cadet_id": None},
            {"id": "u2", "username": "cc_rahul",    "password": "cc123",   "role": "CC",     "name": "Cdt Capt Rahul Dev", "email": "rahul@ncc.in",   "cadet_id": None},
            {"id": "u3", "username": "lc_priya",    "password": "lc123",   "role": "LC",     "name": "Ldg Cdt Priya Nair", "email": "priya@ncc.in",   "cadet_id": "c3"},
            {"id": "u4", "username": "cdt_arjun",   "password": "cdt123",  "role": "Cadet",  "name": "Cdt Arjun Mehta",    "email": "arjun@ncc.in",   "cadet_id": "c1"},
            {"id": "u5", "username": "cdt_sneha",   "password": "cdt123",  "role": "Cadet",  "name": "Cdt Sneha Patel",    "email": "sneha@ncc.in",   "cadet_id": "c2"}
        ],
        "cadets": [
            {"id": "c1", "name": "Arjun Mehta",    "service_number": "KAR/2024/001", "rank": "Cadet",          "platoon": "Alpha",   "contact": "9876543210", "email": "arjun@ncc.in",   "joined": "2024-01-15", "blood_group": "O+"},
            {"id": "c2", "name": "Sneha Patel",    "service_number": "KAR/2024/002", "rank": "Lance Corporal", "platoon": "Alpha",   "contact": "9876543211", "email": "sneha@ncc.in",   "joined": "2024-01-15", "blood_group": "A+"},
            {"id": "c3", "name": "Priya Nair",     "service_number": "KAR/2024/003", "rank": "Corporal",       "platoon": "Bravo",   "contact": "9876543212", "email": "priya@ncc.in",   "joined": "2024-01-15", "blood_group": "B+"},
            {"id": "c4", "name": "Vikram Singh",   "service_number": "KAR/2024/004", "rank": "Sergeant",       "platoon": "Bravo",   "contact": "9876543213", "email": "vikram@ncc.in",  "joined": "2024-02-01", "blood_group": "AB+"},
            {"id": "c5", "name": "Ananya Reddy",   "service_number": "KAR/2024/005", "rank": "Cadet",          "platoon": "Charlie", "contact": "9876543214", "email": "ananya@ncc.in",  "joined": "2024-02-01", "blood_group": "O-"},
            {"id": "c6", "name": "Rohan Gupta",    "service_number": "KAR/2024/006", "rank": "Cadet",          "platoon": "Charlie", "contact": "9876543215", "email": "rohan@ncc.in",   "joined": "2024-02-10", "blood_group": "A-"},
            {"id": "c7", "name": "Deepika Kumar",  "service_number": "KAR/2024/007", "rank": "Lance Corporal", "platoon": "Delta",   "contact": "9876543216", "email": "deepika@ncc.in", "joined": "2024-03-01", "blood_group": "B-"},
            {"id": "c8", "name": "Karan Joshi",    "service_number": "KAR/2024/008", "rank": "Cadet",          "platoon": "Delta",   "contact": "9876543217", "email": "karan@ncc.in",   "joined": "2024-03-01", "blood_group": "O+"}
        ],
        "attendance": {},
        "announcements": [
            {"id": "ann1", "title": "Annual Training Camp 2024",       "body": "Annual Training Camp is scheduled from 15-25 July 2024 at Dharwad. All cadets must report by 0600 hrs in combat uniform with full kit. Attendance is mandatory.", "author": "Lt. Rajiv Sharma",   "role": "ANO", "date": "2024-06-01"},
            {"id": "ann2", "title": "Saturday Parade – This Week",     "body": "This Saturday parade is mandatory for all cadets. Dress: SD Uniform. Time: 0800 hrs sharp. Defaulters will be marked absent.", "author": "Cdt Capt Rahul Dev", "role": "CC",  "date": "2024-06-05"},
            {"id": "ann3", "title": "Republic Day Contingent Selection","body": "Selection for Republic Day Parade contingent will be held on 20 June 2024. All interested cadets with attendance ≥75% are eligible to apply.", "author": "Lt. Rajiv Sharma",   "role": "ANO", "date": "2024-06-10"}
        ],
        "change_requests": []
    }
    save_data(data)
    return data

# ─────────────────────────────────────────────────────────────────────────────
# AUTH DECORATORS
# ─────────────────────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('role') not in roles:
                return jsonify({"error": "Forbidden – insufficient permissions"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

# ─────────────────────────────────────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html',
        user_name=session['name'],
        user_role=session['role'],
        user_id=session['user_id'])

# ─────────────────────────────────────────────────────────────────────────────
# AUTH API
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/login', methods=['POST'])
def api_login():
    data = load_data()
    body = request.json or {}
    user = next((u for u in data['users']
                 if u['username'] == body.get('username')
                 and u['password'] == body.get('password')), None)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401
    session['user_id']  = user['id']
    session['role']     = user['role']
    session['name']     = user['name']
    session['cadet_id'] = user.get('cadet_id')
    return jsonify({
        "role":     user['role'],
        "name":     user['name'],
        "id":       user['id'],
        "cadet_id": user.get('cadet_id')
    })

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({"ok": True})

@app.route('/api/session')
def api_session():
    if 'user_id' not in session:
        return jsonify({"logged_in": False})
    return jsonify({
        "logged_in": True,
        "role":      session['role'],
        "name":      session['name'],
        "id":        session['user_id'],
        "cadet_id":  session.get('cadet_id')
    })

# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD STATS
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/dashboard')
@login_required
def api_dashboard():
    data  = load_data()
    today = date.today().isoformat()
    total = len(data['cadets'])

    today_att = data['attendance'].get(today, {})
    records   = today_att.get('records', {})
    present   = sum(1 for v in records.values() if v == 'P')
    pct       = round((present / total * 100) if total else 0, 1)

    # Overall average across all recorded sessions
    all_dates = list(data['attendance'].keys())
    if all_dates and total:
        total_p = sum(
            sum(1 for v in data['attendance'][d].get('records', {}).values() if v == 'P')
            for d in all_dates
        )
        total_slots = sum(len(data['attendance'][d].get('records', {})) for d in all_dates)
        avg_pct = round((total_p / total_slots * 100) if total_slots else 0, 1)
    else:
        avg_pct = 0.0

    pending_req = sum(1 for r in data['change_requests'] if r['status'] == 'pending')

    return jsonify({
        "total_cadets":    total,
        "present_today":   present,
        "attendance_pct":  pct,
        "avg_pct":         avg_pct,
        "active_users":    len(data['users']),
        "sessions_held":   len(all_dates),
        "pending_requests": pending_req
    })

# ─────────────────────────────────────────────────────────────────────────────
# CADETS
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/cadets', methods=['GET'])
@login_required
def get_cadets():
    data     = load_data()
    role     = session['role']
    cadet_id = session.get('cadet_id')
    if role == 'Cadet' and cadet_id:
        return jsonify([c for c in data['cadets'] if c['id'] == cadet_id])
    return jsonify(data['cadets'])

@app.route('/api/cadets', methods=['POST'])
@login_required
@role_required('ANO', 'CC')
def add_cadet():
    data  = load_data()
    body  = request.json or {}
    new_c = {
        "id":             'c_' + uuid.uuid4().hex[:8],
        "name":           body.get('name', '').strip(),
        "service_number": body.get('service_number', '').strip(),
        "rank":           body.get('rank', 'Cadet'),
        "platoon":        body.get('platoon', 'Alpha'),
        "contact":        body.get('contact', '').strip(),
        "email":          body.get('email', '').strip(),
        "joined":         body.get('joined', date.today().isoformat()),
        "blood_group":    body.get('blood_group', '').strip()
    }
    if not new_c['name'] or not new_c['service_number']:
        return jsonify({"error": "Name and service number are required"}), 400
    data['cadets'].append(new_c)
    save_data(data)
    return jsonify(new_c), 201

@app.route('/api/cadets/<cid>', methods=['PUT'])
@login_required
@role_required('ANO', 'CC')
def update_cadet(cid):
    data = load_data()
    for i, c in enumerate(data['cadets']):
        if c['id'] == cid:
            allowed = ['name','service_number','rank','platoon','contact','email','joined','blood_group']
            for k in allowed:
                if k in (request.json or {}):
                    data['cadets'][i][k] = request.json[k]
            save_data(data)
            return jsonify(data['cadets'][i])
    return jsonify({"error": "Cadet not found"}), 404

@app.route('/api/cadets/<cid>', methods=['DELETE'])
@login_required
@role_required('ANO')
def delete_cadet(cid):
    data = load_data()
    before = len(data['cadets'])
    data['cadets'] = [c for c in data['cadets'] if c['id'] != cid]
    if len(data['cadets']) == before:
        return jsonify({"error": "Cadet not found"}), 404
    save_data(data)
    return jsonify({"ok": True})

# ─────────────────────────────────────────────────────────────────────────────
# ATTENDANCE
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/attendance', methods=['GET'])
@login_required
def get_all_attendance():
    data = load_data()
    return jsonify(data['attendance'])

@app.route('/api/attendance/<att_date>', methods=['GET'])
@login_required
def get_attendance_date(att_date):
    data = load_data()
    return jsonify(data['attendance'].get(att_date, {"records": {}, "frozen": False}))

@app.route('/api/attendance/<att_date>', methods=['POST'])
@login_required
@role_required('ANO', 'CC')
def save_attendance(att_date):
    data     = load_data()
    body     = request.json or {}
    existing = data['attendance'].get(att_date, {"records": {}, "frozen": False})
    if existing.get('frozen') and session['role'] != 'ANO':
        return jsonify({"error": "Attendance is frozen – submit a change request"}), 403
    existing['records'] = body.get('records', existing['records'])
    data['attendance'][att_date] = existing
    save_data(data)
    return jsonify(existing)

@app.route('/api/attendance/<att_date>/submit', methods=['POST'])
@login_required
@role_required('ANO', 'CC')
def submit_attendance(att_date):
    data  = load_data()
    body  = request.json or {}
    entry = {
        "records":      body.get('records', {}),
        "frozen":       True,
        "submitted_by": session['name'],
        "submitted_at": datetime.now().isoformat()
    }
    data['attendance'][att_date] = entry
    save_data(data)
    return jsonify(entry)

@app.route('/api/attendance/<att_date>/unfreeze', methods=['POST'])
@login_required
@role_required('ANO')
def unfreeze_attendance(att_date):
    data = load_data()
    if att_date in data['attendance']:
        data['attendance'][att_date]['frozen'] = False
        save_data(data)
        return jsonify({"ok": True})
    return jsonify({"error": "No attendance record for this date"}), 404

@app.route('/api/attendance/report', methods=['GET'])
@login_required
def attendance_report():
    data     = load_data()
    cadets   = data['cadets']
    role     = session['role']
    cadet_id = session.get('cadet_id')

    if role == 'Cadet' and cadet_id:
        cadets = [c for c in cadets if c['id'] == cadet_id]

    dates  = sorted(data['attendance'].keys())
    report = []
    for c in cadets:
        row = {"cadet": c, "records": {}, "present": 0, "absent": 0, "leave": 0, "total": 0}
        for d in dates:
            rec = data['attendance'][d].get('records', {}).get(c['id'])
            row['records'][d] = rec if rec else '-'
            if rec in ('P', 'A', 'L'):
                row['total'] += 1
                if rec == 'P': row['present'] += 1
                elif rec == 'A': row['absent'] += 1
                elif rec == 'L': row['leave'] += 1
        row['pct'] = round((row['present'] / row['total'] * 100) if row['total'] else 0, 1)
        report.append(row)

    return jsonify({"report": report, "dates": dates})

# ─────────────────────────────────────────────────────────────────────────────
# ANNOUNCEMENTS
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/announcements', methods=['GET'])
@login_required
def get_announcements():
    data = load_data()
    return jsonify(sorted(data['announcements'], key=lambda x: x['date'], reverse=True))

@app.route('/api/announcements', methods=['POST'])
@login_required
@role_required('ANO', 'CC')
def add_announcement():
    data = load_data()
    body = request.json or {}
    if not body.get('title') or not body.get('body'):
        return jsonify({"error": "Title and body are required"}), 400
    ann = {
        "id":     'ann_' + uuid.uuid4().hex[:8],
        "title":  body['title'].strip(),
        "body":   body['body'].strip(),
        "author": session['name'],
        "role":   session['role'],
        "date":   date.today().isoformat()
    }
    data['announcements'].insert(0, ann)
    save_data(data)
    return jsonify(ann), 201

@app.route('/api/announcements/<aid>', methods=['DELETE'])
@login_required
@role_required('ANO', 'CC')
def delete_announcement(aid):
    data   = load_data()
    before = len(data['announcements'])
    data['announcements'] = [a for a in data['announcements'] if a['id'] != aid]
    if len(data['announcements']) == before:
        return jsonify({"error": "Announcement not found"}), 404
    save_data(data)
    return jsonify({"ok": True})

# ─────────────────────────────────────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/users', methods=['GET'])
@login_required
@role_required('ANO')
def get_users():
    data = load_data()
    return jsonify([{k: v for k, v in u.items() if k != 'password'} for u in data['users']])

@app.route('/api/users', methods=['POST'])
@login_required
@role_required('ANO')
def add_user():
    data = load_data()
    body = request.json or {}
    if not body.get('username') or not body.get('password'):
        return jsonify({"error": "Username and password required"}), 400
    if any(u['username'] == body['username'] for u in data['users']):
        return jsonify({"error": "Username already exists"}), 409
    user = {
        "id":       'u_' + uuid.uuid4().hex[:8],
        "username": body['username'].strip(),
        "password": body['password'],
        "role":     body.get('role', 'Cadet'),
        "name":     body.get('name', '').strip(),
        "email":    body.get('email', '').strip(),
        "cadet_id": body.get('cadet_id') or None
    }
    data['users'].append(user)
    save_data(data)
    safe = {k: v for k, v in user.items() if k != 'password'}
    return jsonify(safe), 201

@app.route('/api/users/<uid>', methods=['PUT'])
@login_required
@role_required('ANO')
def update_user(uid):
    data = load_data()
    for i, u in enumerate(data['users']):
        if u['id'] == uid:
            body = request.json or {}
            for k in ['role', 'name', 'email', 'cadet_id']:
                if k in body:
                    data['users'][i][k] = body[k]
            save_data(data)
            return jsonify({k: v for k, v in data['users'][i].items() if k != 'password'})
    return jsonify({"error": "User not found"}), 404

@app.route('/api/users/<uid>', methods=['DELETE'])
@login_required
@role_required('ANO')
def delete_user(uid):
    if uid == session['user_id']:
        return jsonify({"error": "Cannot delete your own account"}), 400
    data   = load_data()
    before = len(data['users'])
    data['users'] = [u for u in data['users'] if u['id'] != uid]
    if len(data['users']) == before:
        return jsonify({"error": "User not found"}), 404
    save_data(data)
    return jsonify({"ok": True})

@app.route('/api/users/<uid>/reset-password', methods=['POST'])
@login_required
@role_required('ANO')
def reset_password(uid):
    data = load_data()
    body = request.json or {}
    pwd  = body.get('password', '').strip()
    if not pwd:
        return jsonify({"error": "New password required"}), 400
    for i, u in enumerate(data['users']):
        if u['id'] == uid:
            data['users'][i]['password'] = pwd
            save_data(data)
            return jsonify({"ok": True})
    return jsonify({"error": "User not found"}), 404

# ─────────────────────────────────────────────────────────────────────────────
# CHANGE REQUESTS
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/change-requests', methods=['GET'])
@login_required
@role_required('ANO', 'CC')
def get_change_requests():
    data = load_data()
    reqs = data['change_requests']
    if session['role'] == 'CC':
        reqs = [r for r in reqs if r.get('requested_by_id') == session['user_id']]
    return jsonify(sorted(reqs, key=lambda x: x.get('created_at', ''), reverse=True))

@app.route('/api/change-requests', methods=['POST'])
@login_required
@role_required('CC')
def create_change_request():
    data = load_data()
    body = request.json or {}
    if not body.get('cadet_id') or not body.get('date') or not body.get('new_status'):
        return jsonify({"error": "cadet_id, date, and new_status required"}), 400
    req = {
        "id":               'cr_' + uuid.uuid4().hex[:8],
        "status":           "pending",
        "cadet_id":         body['cadet_id'],
        "cadet_name":       body.get('cadet_name', ''),
        "date":             body['date'],
        "old_status":       body.get('old_status', '-'),
        "new_status":       body['new_status'],
        "reason":           body.get('reason', '').strip(),
        "requested_by":     session['name'],
        "requested_by_id":  session['user_id'],
        "created_at":       datetime.now().isoformat(),
        "reviewed_at":      None,
        "rejection_note":   None
    }
    data['change_requests'].append(req)
    save_data(data)
    return jsonify(req), 201

@app.route('/api/change-requests/<rid>/approve', methods=['POST'])
@login_required
@role_required('ANO')
def approve_change_request(rid):
    data = load_data()
    for i, r in enumerate(data['change_requests']):
        if r['id'] == rid:
            if r['status'] != 'pending':
                return jsonify({"error": "Request already reviewed"}), 400
            data['change_requests'][i]['status']      = 'approved'
            data['change_requests'][i]['reviewed_at'] = datetime.now().isoformat()
            # Apply the attendance change
            att_date = r['date']
            cid      = r['cadet_id']
            new_val  = r['new_status']
            if att_date in data['attendance']:
                data['attendance'][att_date]['records'][cid] = new_val
            save_data(data)
            return jsonify({"ok": True})
    return jsonify({"error": "Request not found"}), 404

@app.route('/api/change-requests/<rid>/reject', methods=['POST'])
@login_required
@role_required('ANO')
def reject_change_request(rid):
    data = load_data()
    body = request.json or {}
    for i, r in enumerate(data['change_requests']):
        if r['id'] == rid:
            if r['status'] != 'pending':
                return jsonify({"error": "Request already reviewed"}), 400
            data['change_requests'][i]['status']         = 'rejected'
            data['change_requests'][i]['reviewed_at']    = datetime.now().isoformat()
            data['change_requests'][i]['rejection_note'] = body.get('note', '').strip()
            save_data(data)
            return jsonify({"ok": True})
    return jsonify({"error": "Request not found"}), 404

@app.route('/api/change-requests/pending-count')
@login_required
def pending_count():
    data  = load_data()
    count = sum(1 for r in data['change_requests'] if r['status'] == 'pending')
    return jsonify({"count": count})

# ─────────────────────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        init_default_data()
        print("✓ Demo data initialised")
    print("─" * 50)
    print("  NCC Portal – Army Wing")
    print("  http://127.0.0.1:5000")
    print("─" * 50)
    app.run(host='0.0.0.0', port=5000)
