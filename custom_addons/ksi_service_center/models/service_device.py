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
