from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RoomBookingAPI(models.Model):
    _inherit = 'room.booking'

    @api.model
    def get_booking_status(self, booking_id):
        booking = self.env['room.booking'].browse(booking_id)
        if not booking:
            return {'error': 'Pemesanan tidak ditemukan'}
        return {
            'id': booking.id,
            'nomor_pemesanan': booking.name,
            'ruangan': booking.room_id.name,
            'tanggal_pemesanan': booking.booking_date,
            'status': booking.status
        }
