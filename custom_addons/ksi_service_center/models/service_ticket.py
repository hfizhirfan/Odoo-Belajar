from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ServiceTicket(models.Model):
    _name = 'service.ticket'
    _description = 'Tiket Servis & Klaim Garansi'
    _order = 'id desc'

    name = fields.Char(
        string='Nomor Tiket',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: 'Baru'
    )
    customer_name = fields.Char(string='Nama Pelanggan', required=True)
    customer_phone = fields.Char(string='No. Telepon / WhatsApp', required=True)
    customer_email = fields.Char(string='Email')

    device_id = fields.Many2one('service.device', string='Model Perangkat', required=True)
    serial_number = fields.Char(string='Nomor Seri (Serial Number)', required=True)
    purchase_date = fields.Date(string='Tanggal Pembelian')
    warranty_status = fields.Selection([
        ('active', 'Garansi Aktif (Free)'),
        ('expired', 'Garansi Habis (Berbayar)'),
        ('unknown', 'Belum Terverifikasi')
    ], string='Status Garansi', compute='_compute_warranty_status', store=True)

    technician_id = fields.Many2one(
        'res.users',
        string='Teknisi Penanggung Jawab',
        default=lambda self: self.env.user
    )
    date_received = fields.Date(string='Tanggal Masuk', default=fields.Date.context_today)
    date_completed = fields.Date(string='Tanggal Selesai', readonly=True)

    problem_description = fields.Text(string='Keluhan Pelanggan', required=True)
    diagnosis_notes = fields.Text(string='Hasil Diagnosa Teknisi')

    part_ids = fields.One2many('service.ticket.part', 'ticket_id', string='Suku Cadang')
    service_fee = fields.Float(string='Biaya Jasa Servis (Rp)', default=0.0)
    parts_cost = fields.Float(string='Total Suku Cadang (Rp)', compute='_compute_costs', store=True)
    total_cost = fields.Float(string='Total Biaya Akhir (Rp)', compute='_compute_costs', store=True)

    state = fields.Selection([
        ('draft', 'Penerimaan (Draft)'),
        ('in_progress', 'Sedang Dikerjakan'),
        ('waiting_parts', 'Menunggu Suku Cadang'),
        ('done', 'Selesai Diperbaiki'),
        ('delivered', 'Unit Sudah Diambil'),
        ('cancelled', 'Dibatalkan')
    ], string='Status Servis', default='draft', required=True, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Baru') == 'Baru':
            vals['name'] = self.env['ir.sequence'].next_by_code('service.ticket.sequence') or 'Baru'
        return super().create(vals)

    @api.depends('purchase_date', 'device_id.default_warranty_months')
    def _compute_warranty_status(self):
        today = fields.Date.today()
        for ticket in self:
            if not ticket.purchase_date:
                ticket.warranty_status = 'unknown'
                continue
            warranty_months = ticket.device_id.default_warranty_months if ticket.device_id else 12
            expiry_date = ticket.purchase_date + relativedelta(months=warranty_months)
            if today <= expiry_date:
                ticket.warranty_status = 'active'
            else:
                ticket.warranty_status = 'expired'

    @api.depends('part_ids.subtotal', 'service_fee', 'warranty_status')
    def _compute_costs(self):
        for ticket in self:
            total_parts = sum(ticket.part_ids.mapped('subtotal'))
            ticket.parts_cost = total_parts
            # Jika garansi masih aktif, biaya jasa gratis
            fee = 0.0 if ticket.warranty_status == 'active' else ticket.service_fee
            ticket.total_cost = total_parts + fee

    @api.constrains('state', 'diagnosis_notes')
    def _check_diagnosis_before_done(self):
        for ticket in self:
            if ticket.state == 'done' and not ticket.diagnosis_notes:
                raise ValidationError('Harap isi "Hasil Diagnosa Teknisi" sebelum menandai servis selesai!')

    def action_start_repair(self):
        self.write({'state': 'in_progress'})

    def action_wait_parts(self):
        self.write({'state': 'waiting_parts'})

    def action_done(self):
        self.write({
            'state': 'done',
            'date_completed': fields.Date.today()
        })

    def action_deliver(self):
        self.write({'state': 'delivered'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})
