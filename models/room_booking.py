from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class CustomPipelineStage(models.Model):
    _name = 'room.booking.stage'
    _description = 'Pemesanan Ruangan Stages'

    name = fields.Char(string="Stage Name", required=True)
    sequence = fields.Integer(string="Order", default=99)

class RoomBooking(models.Model):
    _name = 'room.booking'
    _description = 'Pemesanan Ruangan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nomor Pemesanan', required=True, copy=False, index=True, default='Baru')
    room_id = fields.Many2one('room.master', string='Ruangan', required=True)
    stage_id = fields.Many2one('room.booking.stage', string="Status Pemesanan", required=True, default=lambda self: self._default_stage())
    booking_name = fields.Char(string='Nama Pemesanan', required=True)
    booking_date = fields.Date(string='Tanggal Pemesanan', required=True)
    notes = fields.Text(string='Catatan Pemesanan')

    @api.model
    def _default_stage(self):
        """Ambil stage dengan sequence terkecil (biasanya Draft) sebagai default"""
        return self.env['room.booking.stage'].search([], order="sequence asc", limit=1).id
    
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
        on_progress = self.env['room.booking.stage'].search(
            [('sequence', '=', 20)], limit=1
        )
        if on_progress:
            self.stage_id = on_progress.id
            self.message_post(body="Stage changed to on Progress", subject="Stage Update")

    def action_done(self):
        done = self.env['room.booking.stage'].search(
            [('sequence', '=', 30)], limit=1
        )
        if done:
            self.stage_id = done.id
            self.message_post(body="Stage changed to Done", subject="Stage Update")

    def action_next_stage(self):
        """Pindah ke stage berikutnya berdasarkan urutan"""
        next_stage = self.env['room.booking.stage'].search(
            [('sequence', '>', self.stage_id.sequence)],
            order="sequence asc", limit=1
        )
        if next_stage:
            self.stage_id = next_stage.id

    def action_previous_stage(self):
        """Kembali ke stage sebelumnya berdasarkan urutan"""
        prev_stage = self.env['room.booking.stage'].search(
            [('sequence', '<', self.stage_id.sequence)],
            order="sequence desc", limit=1
        )
        if prev_stage:
            self.stage_id = prev_stage.id

