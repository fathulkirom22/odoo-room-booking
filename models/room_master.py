from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RoomMaster(models.Model):
    _name = 'room.master'
    _description = 'Master Ruangan'

    name = fields.Char(string='Nama Ruangan', required=True)
    room_type = fields.Selection([
        ('small_meeting', 'Meeting Room Kecil'),
        ('large_meeting', 'Meeting Room Besar'),
        ('hall', 'Aula')
    ], string='Tipe Ruangan', required=True)
    location = fields.Selection([
        ('1A', '1A'), ('1B', '1B'), ('1C', '1C'),
        ('2A', '2A'), ('2B', '2B'), ('2C', '2C')
    ], string='Lokasi Ruangan', required=True)
    photo = fields.Image(string='Foto Ruangan', required=True)
    capacity = fields.Integer(string='Kapasitas Ruangan', required=True)
    description = fields.Text(string='Keterangan')

    _sql_constraints = [
        ('unique_room_name', 'UNIQUE(name)', 'Nama ruangan tidak boleh sama!')
    ]

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing_room = self.env['room.master'].search([
                ('name', '=ilike', record.name),
                ('id', '!=', record.id)
            ])
            if existing_room:
                raise ValidationError('Nama ruangan tidak boleh sama!')