import base64
import hashlib
import jwt
from flask import Flask, render_template, jsonify, request, abort, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kunci-rahasia-facade-labs-ctf-edition-final'
JWT_SECRET = 'jwt-secret-yang-sangat-lemah-dan-mudah-ditebak'

users_data = {
    1: {'username': 'operator_one', 'role': 'operator', 'email': 'op1@facade.tech', 'api_key': 'OPERATOR_API_KEY_01'},
    2: {'username': 'agent_delta', 'role': 'agent', 'email': 'agD@facade.tech', 'api_key': 'AGENT_API_KEY_DELTA'},
    3: {'username': 'admin_zero', 'role': 'admin', 'email': 'adm0@facade.tech', 'api_key': 'ADMIN_SECRET_API_KEY_ZERO'}
}

orders_data = {'a1b2c3d4-e5f6-7777-i9j0-k1l2m3n4o5p6': {'item': 'Laptop X1', 'user_id': 1}, 'b2c3d4e5-f6g7-8888-j0k1-l2m3n4o5p6q7': {'item': 'Mouse Pro', 'user_id': 2}}
invoices_data = {'INV2025001': {'user_id': 1, 'details': 'Invoice Laptop'}, 'INV2025002': {'user_id': 2, 'details': 'Invoice Mouse'}}
files_metadata = {'F101': {'filename': 'op1_report.pdf', 'owner': 1, 'content': 'Laporan rahasia operator'}, 'F102': {'filename': 'agD_notes.txt', 'owner': 2, 'content': 'Catatan agen delta'}, 'F201': {'filename': 'system_config.cfg', 'owner': 3, 'content': 'secret_db_password=123'}}
posts_data = {'P5001': {'title': 'Post Operator', 'author_id': 1}, 'P5002': {'title': 'Post Agent', 'author_id': 2}}
reviews_data = {'prod123': [{'user_id': 1, 'comment': 'Bagus!'}, {'user_id': 2, 'comment': 'Cukup.'}]}
export_jobs = {9000: {'owner_id': 3, 'status': 'DONE'}}
next_job_id = 9001

flags = {
    "s01": f"FL{{{users_data[3]['email']}}}",
    "s02": f"FL{{{orders_data['b2c3d4e5-f6g7-8888-j0k1-l2m3n4o5p6q7']['item'].replace(' ', '_')}}}",
    "s03": f"FL{{{invoices_data['INV2025002']['details'].replace(' ', '_')}}}",
    "s04": f"FL{{{users_data[3]['api_key']}}}",
    "s05": f"FL{{d0cum3nt_acc3ss_by_{users_data[2]['username']}}}",
    "s06": f"FL{{{files_metadata['F201']['filename']}}}",
    "s07": f"FL{{{files_metadata['F201']['content']}}}",
    "s08": "FL{d3l3t3d_an0th3r_us3rs_p0st}",
    "s09": f"FL{{r3vi3w_l34k_{users_data[2]['username']}}}",
    "s10": f"FL{{HTTP_HEADER_ACCESS_{users_data[3]['username']}}}",
    "s11": f"FL{{acc3ss3d_j0b_9000_as_us3r_1}}",
    "s12": f"FL{{JWT_IMP3RS0NATI0N_AS_{users_data[3]['username']}}}",
    "s13": f"FL{{h4sh_cr4ck3d_f0r_{users_data[2]['username']}}}",
    "s14": "FL{R0L3_3SCALATI0N_T0_ADMIN}",
    "s15": f"FL{{w1ldc4rd_inv0ic3_f0und_f0r_us3r_1}}"
}

@app.route('/api/submit_flag', methods=['POST'])
def submit_flag():
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    submitted_flag = data.get('flag')
    correct_flag = flags.get(challenge_id)
    if correct_flag and submitted_flag == correct_flag:
        return jsonify({'correct': True})
    return jsonify({'correct': False})

@app.route('/')
def index(): return render_template('index.html')

@app.route('/challenges')
def challenges(): return render_template('challenges.html')

@app.route('/challenges/numeric')
def challenge_numeric():
    try: user_id = int(request.args.get('id', 1))
    except ValueError: user_id = 1
    user = users_data.get(user_id)
    if not user: abort(404)
    flag_to_show = flags.get("s01") if user_id == 3 else None
    return render_template('challenge_numeric.html', user=user, flag=flag_to_show)

@app.route('/challenges/uuid')
def challenge_uuid():
    order_id = request.args.get('id', 'a1b2c3d4-e5f6-7777-i9j0-k1l2m3n4o5p6')
    order = orders_data.get(order_id)
    if not order: abort(404)
    flag_to_show = flags.get("s02") if order['user_id'] == 2 else None
    return render_template('challenge_uuid.html', order=order, all_orders=orders_data, flag=flag_to_show)

@app.route('/challenges/query')
def challenge_query():
    invoice_id = request.args.get('id', 'INV2025001')
    invoice = invoices_data.get(invoice_id)
    if not invoice: abort(404)
    flag_to_show = flags.get("s03") if invoice['user_id'] == 2 else None
    return render_template('challenge_query.html', invoice=invoice, flag=flag_to_show)

@app.route('/challenges/api_json')
def challenge_api_json_page():
    return render_template('challenge_api_json.html')
@app.route('/api/v1/users/<int:user_id>')
def api_v1_users(user_id):
    user = users_data.get(user_id)
    if not user: return jsonify({'error': 'User not found'}), 404
    if user_id == 3: return jsonify({'user': user, 'flag': flags.get('s04')})
    return jsonify(user)

@app.route('/challenges/base64')
def challenge_base64_page():
    encoded_id = base64.b64encode(b'doc_owner:1').decode('utf-8')
    return render_template('challenge_base64.html', encoded_id=encoded_id)
@app.route('/challenges/base64/doc/<encoded_id>')
def challenge_base64_doc(encoded_id):
    try:
        owner_id = int(base64.b64decode(encoded_id).decode('utf-8').split(':')[1])
        owner = users_data.get(owner_id)
        if not owner: abort(404)
        flag_to_show = flags.get('s05') if owner_id == 2 else None
        return f"<h1>Dokumen Milik: {owner['username']}</h1>" + (f"<p>FLAG: {flag_to_show}</p>" if flag_to_show else "")
    except: abort(400)

@app.route('/challenges/post_body')
def challenge_post_body_page():
    return render_template('challenge_post_body.html')
@app.route('/api/v2/file-metadata', methods=['POST'])
def api_v2_metadata():
    file_id = request.get_json().get('file_id')
    meta = files_metadata.get(file_id)
    if not meta: return jsonify({'error': 'File not found'}), 404
    if file_id == 'F201': return jsonify({'metadata': meta, 'flag': flags.get('s06')})
    return jsonify(meta)

@app.route('/challenges/filename')
def challenge_filename_page():
    return render_template('challenge_filename.html')
@app.route('/challenges/filename/download')
def challenge_filename_download():
    filename = request.args.get('filename')
    for meta in files_metadata.values():
        if meta['filename'] == filename:
            flag_to_show = flags.get('s07') if filename == 'system_config.cfg' else None
            return f"<h1>Konten File: {meta['filename']}</h1><p>{meta['content']}</p>" + (f"<p>FLAG: {flag_to_show}</p>" if flag_to_show else "")
    abort(404)

@app.route('/challenges/blind_action')
def challenge_blind_action_page():
    return render_template('challenge_blind_action.html', posts=posts_data)
@app.route('/challenges/blind_action/delete/<post_id>', methods=['POST'])
def challenge_blind_action_delete(post_id):
    if post_id in posts_data:
        is_other_user_post = posts_data[post_id]['author_id'] != 1
        del posts_data[post_id]
        if is_other_user_post: flash(f"Postingan {post_id} dihapus. FLAG: {flags.get('s08')}", 'success')
        else: flash(f"Postingan {post_id} berhasil dihapus!", 'success')
    else: flash("Postingan tidak ditemukan.", 'error')
    return redirect(url_for('challenge_blind_action_page'))

@app.route('/challenges/secondary_param')
def challenge_secondary_param_page():
    try: user_id = int(request.args.get('reviews_from_user', 1))
    except ValueError: user_id = 1
    reviews = [r for r in reviews_data.get('prod123', []) if r['user_id'] == user_id]
    flag_to_show = flags.get("s09") if user_id == 2 else None
    return render_template('challenge_secondary_param.html', reviews=reviews, user_id=user_id, flag=flag_to_show)

@app.route('/challenges/http_header')
def challenge_http_header_page():
    return render_template('challenge_http_header.html')
@app.route('/api/v3/my-data')
def api_v3_mydata():
    uid = request.headers.get('X-User-ID')
    if not uid or not uid.isdigit(): return jsonify({'error': 'Header X-User-ID tidak valid'}), 400
    user = users_data.get(int(uid))
    if not user: return jsonify({'error': 'User not found'}), 404
    if int(uid) == 3: return jsonify({'user': user, 'flag': flags.get('s10')})
    return jsonify(user)

@app.route('/challenges/multistep')
def challenge_multistep_page():
    return render_template('challenge_multistep.html')
@app.route('/challenges/multistep/export', methods=['POST'])
def challenge_multistep_export():
    global next_job_id
    export_jobs[next_job_id] = {'owner_id': 1, 'status': 'DONE'}
    job_id = next_job_id
    next_job_id += 1
    return jsonify({'job_id': job_id})
@app.route('/challenges/multistep/download')
def challenge_multistep_download():
    job_id = int(request.args.get('job_id'))
    job = export_jobs.get(job_id)
    if not job: abort(404)
    owner = users_data[job['owner_id']]
    flag_to_show = flags.get('s11') if job_id == 9000 else None
    return f"<h1>Data Ekspor Milik: {owner['username']}</h1>" + (f"<p>FLAG: {flag_to_show}</p>" if flag_to_show else "")

@app.route('/challenges/jwt')
def challenge_jwt_page():
    token = jwt.encode({'uid': 2, 'role': 'agent'}, JWT_SECRET, algorithm='HS256')
    return render_template('challenge_jwt.html', token=token)
@app.route('/api/jwt/profile')
def api_jwt_profile():
    token = request.headers.get('Authorization', ' ').split(' ')[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        uid = payload.get('uid')
        if uid == 3: return jsonify({'user': users_data[3], 'flag': flags.get('s12')})
        user = users_data.get(uid)
        if not user: abort(404)
        return jsonify(user)
    except: return jsonify({'error': 'Invalid Token'}), 401

@app.route('/challenges/predictable_hash')
def challenge_predictable_hash_page():
    hashed_id = hashlib.md5(f"1:facade-salt".encode()).hexdigest()
    return render_template('challenge_predictable_hash.html', hashed_id=hashed_id)
@app.route('/challenges/hash/profile/<hashed_id>')
def challenge_predictable_hash_profile(hashed_id):
    for uid, udata in users_data.items():
        if hashlib.md5(f"{uid}:facade-salt".encode()).hexdigest() == hashed_id:
            flag_to_show = flags.get('s13') if uid == 2 else None
            return f"<h1>Profil Pengguna: {udata['username']}</h1>" + (f"<p>FLAG: {flag_to_show}</p>" if flag_to_show else "")
    abort(404)

@app.route('/challenges/mass_assignment')
def challenge_mass_assignment_page():
    return render_template('challenge_mass_assignment.html', user=users_data[2])
@app.route('/api/v4/profile/update', methods=['POST'])
def api_v4_profile_update():
    data = request.get_json()
    user_to_update = users_data.get(2)
    original_role = user_to_update.get('role')
    for key, value in data.items(): user_to_update[key] = value
    if user_to_update.get('role') != original_role and user_to_update.get('role') == 'admin':
        return jsonify({'user': user_to_update, 'flag': flags.get('s14')})
    return jsonify(user_to_update)

@app.route('/challenges/wildcard_api')
def challenge_wildcard_api_page():
    return render_template('challenge_wildcard_api.html')
@app.route('/api/v4/users/<int:user_id>/invoices')
def api_v4_invoices(user_id):
    user_invoices = {k: v for k, v in invoices_data.items() if v['user_id'] == user_id}
    if not user_invoices: return jsonify({'message': f'No invoices found for user {user_id}'}), 404
    flag_to_show = flags.get('s15') if user_id == 1 else None
    return jsonify({'invoices': user_invoices, 'flag': flag_to_show})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)