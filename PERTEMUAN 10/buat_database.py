import sqlite3

try:
    # Koneksi ke database
    sqliteConnection = sqlite3.connect('database_siswa.db')
    cursor = sqliteConnection.cursor()
    print("Database Berhasil terkoneksi")
    
    # Membuat tabel pada database
    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS data_siswa (
                                    id INTEGER PRIMARY KEY,
                                    nama TEXT NOT NULL,
                                    email TEXT NOT NULL UNIQUE);'''
    
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("Tabel berhasil dibuat atau sudah ada")

    # Menambahkan data dummy
    cursor.execute("INSERT INTO data_siswa (nama, email) VALUES ('Najwa', 'najwa@example.com')")
    cursor.execute("INSERT INTO data_siswa (nama, email) VALUES ('Ali', 'ali@example.com')")
    sqliteConnection.commit()
    print("Data awal berhasil dimasukkan")
    
    # Mengecek versi SQLite
    sqlite_select_query = "SELECT sqlite_version();"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("SQLite Database Version is:", record)

except sqlite3.Error as error:
    print("Error Gagal terkoneksi ke Database:", error)

finally:
    if sqliteConnection:
        cursor.close()
        sqliteConnection.close()
        print("Koneksi Database Selesai")
