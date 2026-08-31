from odoo import fields, models


class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Kategori Buku'
    _order = 'name'

    name = fields.Char(string='Nama Kategori', required=True)
    description = fields.Text(string='Deskripsi')
    book_ids = fields.One2many('library.book', 'category_id', string='Buku')
    book_count = fields.Integer(string='Jumlah Buku', compute='_compute_book_count')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Nama kategori harus unik.'),
    ]

    def _compute_book_count(self):
        for category in self:
            category.book_count = len(category.book_ids)


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Buku Perpustakaan'
    _order = 'name'

    name = fields.Char(string='Judul Buku', required=True)
    isbn = fields.Char(string='ISBN')
    author = fields.Char(string='Penulis', required=True)
    publisher = fields.Char(string='Penerbit')
    publication_year = fields.Integer(string='Tahun Terbit')
    category_id = fields.Many2one(
        'library.category', string='Kategori', ondelete='restrict'
    )
    state = fields.Selection([
        ('available', 'Tersedia'),
        ('borrowed', 'Dipinjam'),
    ], string='Status', default='available', required=True, readonly=True)
    active = fields.Boolean(default=True)
    loan_ids = fields.One2many('library.loan', 'book_id', string='Riwayat Peminjaman')

    _sql_constraints = [
        ('isbn_unique', 'unique(isbn)', 'ISBN harus unik.'),
        (
            'publication_year_positive',
            'CHECK(publication_year IS NULL OR publication_year >= 0)',
            'Tahun terbit tidak boleh negatif.',
        ),
    ]
