{
    'name': 'Room Booking',
    'version': '1.7',
    'author': 'Kirom',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/room_booking_sequence.xml',
        'views/action.xml',
        'views/menu.xml',
        'views/room_master_views.xml',
        'views/room_booking_views.xml',
    ],
    'installable': True,
    'application': True,
}