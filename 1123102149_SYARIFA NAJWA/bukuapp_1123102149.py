from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def get_db_connection():
    """Membuat koneksi ke database.

    Returns:
        pymysql.connect: Objek koneksi ke database.
    """
    return pymysql.connect(
        host='localhost',
        user='root',
        password='najwa',  # Pastikan password sesuai dengan pengaturan MySQL Anda
        database='perpus_1123102149'
    )

@app.route('/')
def index():
    """Menampilkan daftar buku dari database.

    Returns:
        render_template: Merender template index_nim.html dengan data buku.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM buku_1123102149")
    buku = cursor.fetchall()
    connection.close()

    return render_template('index_1123102149.html', buku=buku)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        kode_buku = request.form['kode_buku']
        nama_buku = request.form['nama_buku']
        penerbit = request.form['penerbit']
        pengarang = request.form['pengarang']
        jumlah_buku = request.form['jumlah_buku']

        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO buku_1123102149 (Kode_Buku, Nama_Buku, Penerbit, Pengarang, Jumlah_Buku) VALUES (%s, %s, %s, %s, %s)", 
                           (kode_buku, nama_buku, penerbit, pengarang, jumlah_buku))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
        except pymysql.Error as err:
            connection.rollback()
            connection.close()
            return render_template('tambah_1123102149.html', error="Error adding book: " + str(err))

    return render_template('tambah_1123102149.html')

@app.route('/edit/<kode_buku>', methods=['GET', 'POST'])
def edit(kode_buku):
    """Menangani pengeditan informasi buku.

    Args:
        kode_buku (str): Kode Buku yang akan diedit.

    Returns:
        render_template: Merender template edit_nim.html pada GET,
                         mengalihkan ke index pada POST berhasil.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        nama_buku = request.form['nama_buku']
        penerbit = request.form['penerbit']
        pengarang = request.form['pengarang']
        jumlah_buku = request.form['jumlah_buku']

        try:
            cursor.execute("UPDATE buku_1123102149 SET Nama_Buku=%s, Penerbit=%s, Pengarang=%s, Jumlah_Buku=%s WHERE Kode_Buku=%s", 
                           (nama_buku, penerbit, pengarang, jumlah_buku, kode_buku))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
        except pymysql.Error as err:
            connection.rollback()
            connection.close()
            return render_template('edit_1123102149.html', book=buku, error="Error updating book: " + str(err))

    cursor.execute("SELECT * FROM buku_1123102149 WHERE Kode_Buku=%s", (kode_buku,))
    buku = cursor.fetchone()
    connection.close()

    return render_template('edit_1123102149.html', book=buku)

if __name__ == '__main__':
    app.run(debug=True)
