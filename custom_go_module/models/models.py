from odoo import models, fields, api

class GO(models.Model):
    _name = 'custom_go_module.go'
    _description = 'Generación de Órdenes'

    name = fields.Char(string='Nombre', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('custom_go_module.go.seq'))

    manufacturing_order_id = fields.Many2one('mrp.production', string='Orden de Fabricación')
    sales_order_id = fields.Many2one('sale.order', string='Orden de Venta')
    quantity = fields.Float(string='Cantidad')
    deadline_date = fields.Date(string='Fecha límite de fabricación')

    # Obtención de las órdenes de fabricación relacionadas con una orden de venta
    @api.onchange('sales_order_id')
    def get_manufacturing_orders(self):
        if self.sales_order_id:
            manufacturing_orders = self.env['mrp.production'].search([('origin', '=', self.sales_order_id.name)])
            # Asignar las órdenes de fabricación encontradas al registro actual
            self.manufacturing_order_id = [(6, 0, manufacturing_orders.ids)]
           

    

