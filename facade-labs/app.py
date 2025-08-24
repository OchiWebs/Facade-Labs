# ==============================================================================
# FACADE-LABS v3 - FINAL APP.PY
# Dibuat oleh: ThisOchi
# Deskripsi: Backend lengkap untuk 15 simulasi IDOR dengan tingkat kesulitan beragam.
# ==============================================================================

import base64
import hashlib
import jwt
from flask import Flask, render_template, jsonify, request, abort, redirect, url_for, flash

# === KONFIGURASI & SETUP ===
app = Flask(__name__)
app.config['SECRET_KEY'] = 'kunci-rahasia-facade-labs-by-thisochi-v3-final'
JWT_SECRET = 'jwt-secret-yang-sangat-lemah-dan-mudah-ditebak'

# === DATABASE SIMULASI ===
users_data = {
    1: {'username': 'operator_one', 'role': 'operator', 'email': 'op1@facade.tech'},
    2: {'username': 'agent_delta', 'role': 'agent', 'email': 'agD@facade.tech'},
    3: {'username': 'admin_zero', 'role': 'admin', 'email': 'adm0@facade.tech'}
}
orders_data = {'a1b2c3d4-e5f6-7777-i9j0-k1l2m3n4o5p6': {'item': 'Laptop X1', 'user_id': 1}, 'b2c3d4e5-f6g7-8888-j0k1-l2m3n4o5p6q7': {'item': 'Mouse Pro', 'user_id': 2}}
invoices_data = {'INV2025001': {'user_id': 1, 'details': 'Invoice Laptop'}, 'INV2025002': {'user_id': 2, 'details': 'Invoice Mouse'}}
files_metadata = {'F101': {'filename': 'op1_report.pdf', 'owner': 1, 'content': 'Laporan rahasia operator'}, 'F102': {'filename': 'agD_notes.txt', 'owner': 2, 'content': 'Catatan agen delta'}, 'F201': {'filename': 'system_config.cfg', 'owner': 3, 'content': 'Konfigurasi sistem admin'}}
posts_data = {'P5001': {'title': 'Post Operator', 'author_id': 1}, 'P5002': {'title': 'Post Agent', 'author_id': 2}}
reviews_data = {'prod123': [{'user_id': 1, 'comment': 'Bagus!'}, {'user_id': 2, 'comment': 'Cukup.'}]}
export_jobs = {}
next_job_id = 9001

# === HALAMAN UTAMA & DASBOR ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulations')
def simulations():
    return render_template('simulations.html')

# ==============================================================================
# === [FOUNDATION TIER] SIMULASI 1-5 ===
# ==============================================================================

# --- SIMULASI 1: IDOR NUMERIK ---
@app.route('/simulations/numeric/profile/<int:user_id>')
def sim_01_numeric_page(user_id):
    user = users_data.get(user_id)
    if not user: abort(404)
    return render_template('sim_01_numeric.html', user=user)

# --- SIMULASI 2: IDOR UUID ---
@app.route('/simulations/uuid/order/<uuid>')
def sim_02_uuid_page(uuid):
    order = orders_data.get(uuid)
    if not order: abort(404)
    return render_template('sim_02_uuid.html', order=order, all_orders=orders_data)

# --- SIMULASI 3: IDOR QUERY PARAMETER ---
@app.route('/simulations/query/invoice')
def sim_03_query_page():
    invoice_id = request.args.get('id')
    invoice = invoices_data.get(invoice_id)
    if not invoice: abort(404)
    return render_template('sim_03_query.html', invoice=invoice, invoice_id=invoice_id)

# --- SIMULASI 4: IDOR API JSON ---
@app.route('/simulations/api-json')
def sim_04_api_json_page():
    return render_template('sim_04_api_json.html')
@app.route('/api/v1/users/<int:user_id>')
def sim_04_api_endpoint(user_id):
    user = users_data.get(user_id)
    if not user: return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

# --- SIMULASI 5: IDOR BASE64 ---
@app.route('/simulations/base64/doc/<encoded_id>')
def sim_05_base64_page(encoded_id):
    try:
        doc_id_str = base64.b64decode(encoded_id).decode('utf-8')
        doc_owner_id = int(doc_id_str.split(':')[1])
        owner = users_data.get(doc_owner_id)
        if not owner: abort(404)
        return render_template('sim_05_base64.html', owner=owner)
    except: abort(400, "Invalid Base64 ID")

# ==============================================================================
# === [ADVANCED TIER] SIMULASI 6-10 ===
# ==============================================================================

# --- SIMULASI 6: IDOR POST BODY ---
@app.route('/simulations/post-body')
def sim_06_post_body_page():
    return render_template('sim_06_post_body.html')
@app.route('/api/v2/file-metadata', methods=['POST'])
def sim_06_api_endpoint():
    data = request.get_json()
    file_id = data.get('file_id')
    meta = files_metadata.get(file_id)
    if not meta: return jsonify({'error': 'File not found'}), 404
    return jsonify(meta)

# --- SIMULASI 7: IDOR FILENAME ---
@app.route('/simulations/filename')
def sim_07_filename_page():
    return render_template('sim_07_filename.html')
@app.route('/simulations/filename/download')
def sim_07_download_endpoint():
    filename = request.args.get('filename')
    for meta in files_metadata.values():
        if meta['filename'] == filename:
            return f"<h1>Konten File: {meta['filename']}</h1><p>{meta['content']}</p>"
    abort(404, "File not found")

# --- SIMULASI 8: BLIND ACTION IDOR ---
@app.route('/simulations/blind-action')
def sim_08_blind_action_page():
    return render_template('sim_08_blind_action.html', data={'blind_action_posts': posts_data})
@app.route('/simulations/blind-action/post/delete/<post_id>', methods=['POST'])
def sim_08_delete_endpoint(post_id):
    if post_id in posts_data:
        del posts_data[post_id]
        flash(f"Postingan {post_id} berhasil dihapus!", 'success')
    else:
        flash(f"Postingan {post_id} tidak ditemukan.", 'error')
    return redirect(url_for('sim_08_blind_action_page'))

# --- SIMULASI 9: IDOR SECONDARY PARAMETER ---
@app.route('/simulations/secondary-param/product/<prod_id>')
def sim_09_secondary_param_page(prod_id):
    try:
        user_filter_id = int(request.args.get('reviews_from_user', 1))
    except ValueError:
        user_filter_id = 1
    all_reviews = reviews_data.get(prod_id, [])
    filtered = [r for r in all_reviews if r['user_id'] == user_filter_id]
    return render_template('sim_09_secondary_param.html', reviews=filtered, user_id=user_filter_id)

# --- SIMULASI 10: IDOR HTTP HEADER ---
@app.route('/simulations/http-header')
def sim_10_http_header_page():
    return render_template('sim_10_http_header.html')
@app.route('/api/v3/my-data')
def sim_10_api_endpoint():
    user_id_header = request.headers.get('X-User-ID')
    if not user_id_header or not user_id_header.isdigit():
        return jsonify({'error': 'Header X-User-ID tidak valid atau tidak ada'}), 400
    user = users_data.get(int(user_id_header))
    if not user: return jsonify({'error': 'User not found based on header'}), 404
    return jsonify(user)

# ==============================================================================
# === [EXPERT TIER] SIMULASI 11-15 ===
# ==============================================================================

# --- SIMULASI 11: MULTI-STEP IDOR ---
@app.route('/simulations/multistep')
def sim_11_multistep_page():
    return render_template('sim_11_multistep.html')
@app.route('/simulations/multistep/export', methods=['POST'])
def sim_11_export_endpoint():
    global next_job_id
    job_id = next_job_id
    # Vulnerability: job owner is hardcoded, but in a real app would be from a session
    export_jobs[job_id] = {'owner_id': 1, 'status': 'DONE'}
    next_job_id += 1
    return jsonify({'job_id': job_id, 'status': 'DONE'})
@app.route('/simulations/multistep/download')
def sim_11_download_endpoint():
    job_id = int(request.args.get('job_id'))
    job = export_jobs.get(job_id)
    if not job: abort(404)
    # VULN: No check if the current user is job['owner_id']
    owner = users_data[job['owner_id']]
    return f"<h1>Data ekspor sensitif</h1><p>Ini adalah data milik <b>{owner['username']}</b></p>"

# --- SIMULASI 12: IDOR JWT PAYLOAD ---
@app.route('/simulations/jwt')
def sim_12_jwt_page():
    # Generate a default token for the logged-in user (agent_delta, uid: 2)
    token = jwt.encode({'uid': 2, 'role': 'agent'}, JWT_SECRET, algorithm='HS256')
    return render_template('sim_12_jwt.html', data={'jwt_token_user_2': token})
@app.route('/api/jwt/profile')
def sim_12_api_endpoint():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '): return jsonify({'error': 'Header otorisasi tidak ada'}), 401
    token = auth_header.split(" ")[1]
    try:
        # VULN: Trusts the uid from the payload without further validation
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = users_data.get(payload['uid'])
        if not user: abort(404)
        return jsonify(user)
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid Token'}), 401

# --- SIMULASI 13: IDOR PREDICTABLE HASH ---
@app.route('/simulations/predictable-hash')
def sim_13_hash_page():
    # Provide the link for the first user
    hashed_id = hashlib.md5(f"1:facade-salt".encode()).hexdigest()
    return render_template('sim_13_predictable_hash.html', hashed_id=hashed_id)
@app.route('/simulations/hash/profile/<hashed_id>')
def sim_13_profile_endpoint(hashed_id):
    for uid, udata in users_data.items():
        # VULN: Predictable salt and algorithm
        expected_hash = hashlib.md5(f"{uid}:facade-salt".encode()).hexdigest()
        if expected_hash == hashed_id:
            return f"<h1>Profil Pengguna</h1><p>Berhasil mengakses profil untuk <b>{udata['username']}</b>.</p>"
    abort(404)

# --- SIMULASI 14: IDOR MASS ASSIGNMENT ---
@app.route('/simulations/mass-assignment')
def sim_14_mass_assignment_page():
    return render_template('sim_14_mass_assignment.html', data={'mass_assignment_user': users_data[2]})
@app.route('/api/v4/profile/update', methods=['POST'])
def sim_14_api_endpoint():
    data = request.get_json()
    # Assume user 2 is logged in and is the only one they can update.
    user_to_update = users_data.get(2)
    # VULN: Directly updating object from user-controlled JSON, allowing role escalation.
    for key, value in data.items():
        if key in user_to_update:
            user_to_update[key] = value
    return jsonify(user_to_update)

# --- SIMULASI 15: IDOR WILDCARD API ---
@app.route('/simulations/wildcard-api')
def sim_15_wildcard_api_page():
    return render_template('sim_15_wildcard_api.html')
@app.route('/api/v4/users/<int:user_id>/invoices')
def sim_15_api_endpoint(user_id):
    # VULN: Endpoint meant for admins is exposed.
    user_invoices = {k: v for k, v in invoices_data.items() if v['user_id'] == user_id}
    if not user_invoices: return jsonify({'message': f'No invoices found for user {user_id}'}), 404
    return jsonify(user_invoices)

# === RUNNER ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)