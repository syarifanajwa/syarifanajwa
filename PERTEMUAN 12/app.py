from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Tentukan folder untuk menyimpan file yang diupload
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tentukan ekstensi file yang diizinkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'bmp'}

# Fungsi untuk memeriksa ekstensi file yang diupload
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Buat folder uploads jika belum ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            # Periksa apakah file ada dalam request
            if 'file' not in request.files:
                return 'No file part in the request.'
            file = request.files['file']

            # Jika tidak ada file yang dipilih
            if file.filename == '':
                return 'No selected file. Please choose a file.'

            # Jika file memiliki ekstensi yang diizinkan
            if file and allowed_file(file.filename):
                # Simpan file ke dalam folder uploads
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                return f'File successfully uploaded to {filename}'
            else:
                return 'Invalid file type. Allowed types are png, jpg, jpeg, gif, pdf, bmp.'
        except Exception as e:
            return f"Error: {str(e)}"  # Tampilkan error di browser jika ada
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
