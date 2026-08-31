from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Master Data Pasien'

    name = fields.Char(string='Nama Pasien', required=True)
    age = fields.Integer(string='Umur')
    gender = fields.Selection([
        ('male', 'Laki-Laki'),
        ('female', 'Perempuan')
    ], string='Jenis Kelamin')