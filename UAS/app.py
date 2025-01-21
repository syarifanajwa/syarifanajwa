from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia Anda

# MongoDB Client
client = MongoClient('mongodb://localhost:27017/')
db = client['crud_mobil']
collection = db['rental_mobil']

# Konfigurasi folder upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    cars = collection.find()
    return render_template('index.html', cars=cars)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Username atau password salah!', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('index'))


@app.route('/admin')
def admin_dashboard():
    if not session.get('logged_in'):
        flash('Anda harus login terlebih dahulu.', 'warning')
        return redirect(url_for('login'))

    cars = collection.find()
    return render_template('admin.html', cars=cars)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if not session.get('logged_in'):
        flash('Anda harus login terlebih dahulu.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        nama = request.form['nama']
        harga_perhari = request.form['harga_perhari']
        kecepatan = request.form['kecepatan']
        stok = request.form['stok']

        foto = request.files['foto']
        if foto and allowed_file(foto.filename):
            filename = secure_filename(f"{uuid.uuid4()}_{foto.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(filepath)
        else:
            filename = None

        collection.insert_one({
            'nama': nama,
            'harga_perhari': harga_perhari,
            'kecepatan': kecepatan,
            'stok': stok,
            'foto': filename
        })
        return redirect(url_for('admin_dashboard'))

    return render_template('add.html')


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    try:
        # Ambil data user berdasarkan ID
        user = collection.find_one({'_id': ObjectId(id)})

        if request.method == 'POST':
            nama = request.form['nama']
            harga_perhari = request.form['harga_perhari']
            kecepatan = request.form['kecepatan']
            stok = request.form['stok']

            # Menangani unggahan foto
            foto = request.files['foto']
            if foto and allowed_file(foto.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{foto.filename}")  # Nama unik
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(filepath)

                # Hapus foto lama jika ada
                if user.get('foto'):
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], user['foto'])
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
            else:
                filename = user.get('foto')  # Gunakan foto lama jika tidak ada yang baru

            # Update data di MongoDB
            collection.update_one(
                {'_id': ObjectId(id)},
                {'$set': {
                    'nama': nama,
                    'harga_perhari': harga_perhari,
                    'kecepatan': kecepatan,
                    'stok': stok,
                    'foto': filename
                }}
            )
            return redirect(url_for('admin_dashboard'))

        return render_template('edit.html', user=user)

    except Exception as e:
        print(f"Error: {e}")
        return "Terjadi kesalahan saat mengedit data.", 500

@app.route('/delete/<id>')
def delete(id):
    user = collection.find_one({'_id': ObjectId(id)})
    
    # Hapus foto dari folder jika ada
    if user.get('foto'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user['foto'])
        if os.path.exists(file_path):
            os.remove(file_path)
    
    # Hapus data dari MongoDB
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('admin_dashboard'))

@app.route('/add_manual')
def add_manual():
    # Contoh data mobil dengan foto default
    collection.insert_one({
        'nama': 'Toyota Avanza',
        'harga_perhari': 500000,
        'kecepatan': 120,
        'stok': 10,
        'foto': 'car1.jpg'  # Nama file gambar yang ada di folder static/img
    })
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
