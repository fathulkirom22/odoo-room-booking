from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class RoomBooking(models.Model):
    _name = 'room.booking'
    _description = 'Pemesanan Ruangan'

    name = fields.Char(string='Nomor Pemesanan', required=True, copy=False, index=True, default='-')
    room_id = fields.Many2one('room.master', string='Ruangan', required=True)
    booking_name = fields.Char(string='Nama Pemesanan', required=True)
    booking_date = fields.Datetime(string='Tanggal Pemesanan', required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('on_going', 'On Going'),
        ('done', 'Done')
    ], string='Status Pemesanan', default='draft')
    notes = fields.Text(string='Catatan Pemesanan')

    @api.constrains('room_id', 'booking_date')
    def _check_duplicate_booking(self):
        for record in self:
            existing_booking = self.env['room.booking'].search([
                ('room_id', '=', record.room_id.id),
                ('booking_date', '=', record.booking_date),
                ('id', '!=', record.id)
            ])
            if existing_booking:
                raise ValidationError('Ruangan sudah dipesan untuk tanggal tersebut!')

    @api.constrains('booking_name')
    def _check_duplicate_booking_name(self):
        for record in self:
            existing_booking = self.env['room.booking'].search([
                ('booking_name', '=', record.booking_name),
                ('id', '!=', record.id)
            ])
            if existing_booking:
                raise ValidationError('Nama pemesanan tidak boleh sama!')

    @api.model_create_multi
    def create(self, vals_list):
        """ Override create() untuk mendukung batch processing """
        for vals in vals_list:
            # Ambil tanggal pemesanan dengan format aman
            booking_date = vals.get('booking_date')
            if booking_date:
                date_str = datetime.strptime(str(booking_date)[:10], "%Y-%m-%d").strftime("%Y%m%d")
            else:
                date_str = datetime.today().strftime("%Y%m%d")

            # Ambil informasi ruangan (pastikan ID valid)
            room_id = vals.get('room_id')
            room = self.env['room.master'].browse(room_id) if room_id else None
            if not room or not room.exists():
                raise ValidationError("Ruangan tidak ditemukan!")

            # Pemetaan kode tipe ruangan
            room_type_map = {
                'small_meeting': 'MRK',
                'large_meeting': 'MRB',
                'hall': 'AUL'
            }
            room_type_code = room_type_map.get(room.room_type, 'XXX')

            # Tentukan Tipe Pemesanan
            booking_type = "MEETING" if room.room_type != 'hall' else "TOWNHALL"

            # Generate sequence
            sequence = self.env['ir.sequence'].next_by_code('room.booking') or '00000'

            # Format Nomor Pemesanan
            vals['name'] = f"{booking_type}-{room_type_code}-{date_str}-{sequence}"

        return super().create(vals_list)

    def action_confirm(self):
        self.status = 'on_going'

    def action_done(self):
        self.status = 'done'

