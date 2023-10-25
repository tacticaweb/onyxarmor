
from odoo import fields,models,api


class res_config(models.TransientModel): 
    _inherit='res.config.settings'
        
    lot_serial_method = fields.Selection([('today_date','Today Date'), ('production_date', 'Production Date')],default='today_date',string='Lot/Serial number Applied based On')
    
    @api.model
    def get_values(self):
        res = super(res_config, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res['lot_serial_method'] = params.get_param('mai_auto_lotserial_mrp_workorder.lot_serial_method',default='today_date')
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('mai_auto_lotserial_mrp_workorder.lot_serial_method', self.lot_serial_method)
        super(res_config,self).set_values()