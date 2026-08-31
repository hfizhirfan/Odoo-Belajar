from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Peminjaman Buku'
    _order = 'loan_date desc, id desc'

    name = fields.Char(
        string='Nomor Peminjaman', default='Baru', readonly=True, copy=False
    )
    member_id = fields.Many2one(
        'library.member', string='Anggota', required=True, ondelete='restrict'
    )
    book_id = fields.Many2one(
        'library.book', string='Buku', required=True, ondelete='restrict'
    )
    loan_date = fields.Date(
        string='Tanggal Pinjam', required=True, default=fields.Date.context_today
    )
    due_date = fields.Date(string='Jatuh Tempo', required=True)
    return_date = fields.Date(string='Tanggal Kembali', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Dipinjam'),
        ('returned', 'Dikembalikan'),
        ('cancelled', 'Dibatalkan'),
    ], string='Status', default='draft', required=True, readonly=True)
    days_late = fields.Integer(string='Hari Terlambat', compute='_compute_late_values')
    fine_amount = fields.Float(string='Denda', compute='_compute_late_values')

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        loan_date = values.get('loan_date') or fields.Date.context_today(self)
        if 'due_date' in fields_list and not values.get('due_date'):
            values['due_date'] = fields.Date.to_date(loan_date) + timedelta(days=7)
        return values

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get('name', 'Baru') == 'Baru':
                values['name'] = self.env['ir.sequence'].next_by_code('library.loan') or 'Baru'
        return super().create(vals_list)

    @api.depends('due_date', 'return_date', 'state')
    def _compute_late_values(self):
        today = fields.Date.context_today(self)
        for loan in self:
            comparison_date = loan.return_date or today
            loan.days_late = (
                max((comparison_date - loan.due_date).days, 0)
                if loan.due_date and loan.state in ('borrowed', 'returned')
                else 0
            )
            loan.fine_amount = loan.days_late * 2000.0

    @api.constrains('loan_date', 'due_date')
    def _check_due_date(self):
        for loan in self:
            if loan.loan_date and loan.due_date and loan.due_date < loan.loan_date:
                raise ValidationError(_('Tanggal jatuh tempo tidak boleh sebelum tanggal pinjam.'))

    def action_borrow(self):
        for loan in self:
            if loan.book_id.state != 'available':
                raise UserError(_('Buku "%s" sedang tidak tersedia.') % loan.book_id.name)
            loan.write({'state': 'borrowed'})
            loan.book_id.state = 'borrowed'

    def action_return(self):
        for loan in self:
            if loan.state != 'borrowed':
                raise UserError(_('Hanya peminjaman aktif yang dapat dikembalikan.'))
            loan.write({
                'state': 'returned',
                'return_date': fields.Date.context_today(self),
            })
            loan.book_id.state = 'available'

    def action_cancel(self):
        for loan in self:
            if loan.state == 'borrowed':
                loan.book_id.state = 'available'
            loan.state = 'cancelled'
