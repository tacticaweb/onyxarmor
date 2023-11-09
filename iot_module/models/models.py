from odoo import models, fields

class RFID(models.Model):
    _name = 'rfid.data'
    _description = 'RFID Data'

    csn = fields.Char(string='CSN', required=True)
    etapa = fields.Char(string='ETAPA', required=True)
    fecha = fields.Datetime(string='FECHA', default=lambda self: fields.Datetime.now(), required=True)

