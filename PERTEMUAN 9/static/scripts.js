// scripts.js

$(document).ready(function() {
    // Menutup modal setelah form disubmit
    $('#modal-tambah form').on('submit', function(e) {
        setTimeout(function() {
            $('#modal-tambah').modal('hide');
        }, 500); // Menunggu setengah detik untuk memastikan form terkirim
    });

    $('#modal-edit').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var id = button.data('id');
        var nama = button.data('nama');
        var alamat = button.data('alamat');
        var jurusan = button.data('jurusan');
        var nohp = button.data('nohp');

        var modal = $(this);
        modal.find('.modal-body #nama').val(nama);
        modal.find('.modal-body #alamat').val(alamat);
        modal.find('.modal-body #jurusan').val(jurusan);
        modal.find('.modal-body #nohp').val(nohp);
        modal.find('.modal-body #id').val(id);
    });
});
