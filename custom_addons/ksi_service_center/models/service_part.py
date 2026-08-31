from odoo import api, fields, models


class ServiceTicketPart(models.Model):
    _name = 'service.ticket.part'
    _description = 'Penggunaan Suku Cadang Servis'

    ticket_id = fields.Many2one('service.ticket', string='Tiket Servis', ondelete='cascade', required=True)
    name = fields.Char(string='Nama Komponen / Spare Part', required=True)
    part_code = fields.Char(string='Kode Part / SKU')
    quantity = fields.Integer(string='Jumlah (Qty)', default=1, required=True)
    price_unit = fields.Float(string='Harga Satuan (Rp)', required=True)
    subtotal = fields.Float(string='Subtotal (Rp)', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
