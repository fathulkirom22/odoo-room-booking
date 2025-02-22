from odoo import http
from odoo.http import request
import json

class RoomBookingAPI(http.Controller):

    @http.route('/api/booking/<string:nomor_pesanan>', auth='public', methods=['GET'], type='http')
    def get_booking_status(self, nomor_pesanan):
        """Mendapatkan status pemesanan ruangan berdasarkan ID"""
        booking = request.env['room.booking'].sudo().search([('name', '=', nomor_pesanan)], limit=1)
        if not booking.exists():
            return request.make_response(
                json.dumps({'error': 'Pemesanan tidak ditemukan'}), 
                headers=[('Content-Type', 'application/json')]
            )

        data = {
            'id': booking.id,
            'nomor_pemesanan': booking.name,
            'ruangan': booking.room_id.name,
            'tanggal_pemesanan': booking.booking_date.isoformat(),
            'status': booking.status
        }

        res = {'status': 'success', 'data': data}

        return request.make_response(
            json.dumps(res), 
            headers=[('Content-Type', 'application/json')]
        )
