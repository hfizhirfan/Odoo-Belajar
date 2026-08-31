from odoo import fields, models


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Anggota Perpustakaan'
    _order = 'name'

    name = fields.Char(string='Nama Anggota', required=True)
    member_number = fields.Char(string='Nomor Anggota', required=True, copy=False)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Nomor Telepon')
    address = fields.Text(string='Alamat')
    active = fields.Boolean(default=True)
    loan_ids = fields.One2many('library.loan', 'member_id', string='Peminjaman')
    active_loan_count = fields.Integer(
        string='Buku Sedang Dipinjam', compute='_compute_active_loan_count'
    )

    _sql_constraints = [
        ('member_number_unique', 'unique(member_number)', 'Nomor anggota harus unik.'),
    ]

    def _compute_active_loan_count(self):
        for member in self:
            member.active_loan_count = len(
                member.loan_ids.filtered(lambda loan: loan.state == 'borrowed')
            )
