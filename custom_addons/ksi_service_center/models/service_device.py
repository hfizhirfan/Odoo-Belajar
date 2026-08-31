from odoo import fields, models


class ServiceDevice(models.Model):
    _name = 'service.device'
    _description = 'Master Model Perangkat / Laptop'
    _order = 'name'

    name = fields.Char(string='Model Perangkat', required=True)
    brand = fields.Char(string='Brand / Merk', default='Axioo', required=True)
    device_type = fields.Selection([
        ('laptop', 'Laptop / Notebook'),
        ('desktop', 'Desktop PC / AIO'),
        ('tablet', 'Tablet / 2-in-1'),
        ('other', 'Aksesoris / Lainnya')
    ], string='Tipe Perangkat', default='laptop', required=True)
    default_warranty_months = fields.Integer(string='Garansi Default (Bulan)', default=12)
    description = fields.Text(string='Spesifikasi Singkat')
    active = fields.Boolean(default=True)
    ticket_ids = fields.One2many('service.ticket', 'device_id', string='Tiket Servis')
    ticket_count = fields.Integer(string='Jumlah Servis', compute='_compute_ticket_count')

    def _compute_ticket_count(self):
        for device in self:
            device.ticket_count = len(device.ticket_ids)

    def action_view_tickets(self):
        self.ensure_one()
        return {
            'name': f'Riwayat Servis: {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'service.ticket',
            'view_mode': 'kanban,tree,form',
            'domain': [('device_id', '=', self.id)],
            'context': {'default_device_id': self.id},
        }
