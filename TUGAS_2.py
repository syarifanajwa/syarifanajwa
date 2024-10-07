def hitung_gaji(nama, golongan, jam_kerja):
    if golongan == 'A':
        upah_per_jam = 5000
    elif golongan == 'B':
        upah_per_jam = 7000
    elif golongan == 'C':
        upah_per_jam = 8000
    elif golongan == 'D':
        upah_per_jam = 10000
    else:
        return "Golongan tidak valid"
    
    upah_reguler = upah_per_jam * jam_kerja

    if jam_kerja > 48:
        uang_lembur = (jam_kerja - 48) * 4000
    else:
        uang_lembur = 0

    total_gaji = upah_reguler + uang_lembur


    return f"Karyawan: {nama}, Golongan: {golongan}, Gaji Total: Rp. {total_gaji}"
nama = input("Masukkan nama Karyawan:")
golongan = input("Masukkan golongan karyawan (A/B/C/D):").upper()
jam_kerja = int(input("Masukkan jumlah jam kerja:"))

hasil = hitung_gaji(nama, golongan, jam_kerja)
print(hasil)