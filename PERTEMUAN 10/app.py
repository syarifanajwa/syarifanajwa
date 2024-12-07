from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
import sqlite3
app=Flask(__name__)

@app.route("/")
#INDEX
@app.route("/index")
def index():
    sqliteConnection = sqlite3.connect('database_siswa.db')
    cursor = sqliteConnection.cursor()
    cursor.row_factory=sql.Row
    sqlite_select_query = """SELECT * from data_siswa"""
    cursor.execute(sqlite_select_query)
    data = cursor.fetchall()
    return render_template("index.html",datas=data)

#TAMBAH
@app.route("/tambah_data",methods=['POST','GET'])
def tambah_data():
    if request.method=='POST':
        nama=request.form['nama']
        email=request.form['email']
        sqliteConnection = sqlite3.connect('database_siswa.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("insert into data_siswa(nama,email) values (?,?)",(nama,email))
        sqliteConnection.commit()
        flash('Data Sudah Masuk','success')
        return redirect(url_for("index"))
    return render_template("tambah_data.html")

#EDIT
@app.route("/edit_data/<string:id>",methods=['POST','GET'])
def edit_data(id):
    if request.method=='POST':
        nama=request.form['nama']
        email=request.form['email']
        sqliteConnection = sqlite3.connect('database_siswa.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("update data_siswa set nama=?, email=? where id=?",(nama,email,id))
        sqliteConnection.commit()
        flash('Data Sudah Di Update','success')
        return redirect(url_for("index"))
    
    sqliteConnection = sqlite3.connect('database_siswa.db')
    cursor = sqliteConnection.cursor()
    cursor.row_factory=sql.Row
    cursor.execute("select * from data_siswa where id=?",(id,))
    data=cursor.fetchone()
    return render_template("edit_data.html",datas=data)

#HAPUS
@app.route("/hapus_data/<string:id>",methods=['GET'])
def hapus_data(id):
    sqliteConnection = sqlite3.connect('database_siswa.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("delete from data_siswa where id=?",(id,))
    sqliteConnection.commit()
    flash('Data Sudah Terhapus','warning')
    return redirect(url_for("index"))

if __name__=='__main__':
    app.secret_key='stikom123'
    app.run(debug=True)