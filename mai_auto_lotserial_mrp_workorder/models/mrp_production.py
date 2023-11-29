from odoo import fields,models,api,_
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
import math
from datetime import datetime
import time
from odoo.exceptions import ValidationError

class mrp_production_al(models.Model):
    _inherit="mrp.production"
    
    mrp_lot_id=fields.Many2one('stock.production.lot', string='MRP Lot',copy=False)
    
    # @api.multi
    def open_produce_product(self):
        date = datetime.now().strftime('%Y%m%d%H')        
        if self.mrp_lot_id:
            res= super(mrp_production_al,self).open_produce_product()
        else:
            counter=1
            lot_id_name = date
            lot_ids=self.env['stock.production.lot'].search([('name',"ilike",date)])
            if lot_ids:
                for lot in lot_ids:
                    counter+=1
                lot_id_name=date+"000"+str(counter)
            else:
                lot_id_name=date+"0001"
            vals={
                    "product_id":self.product_id.id,
                    "name":lot_id_name,
                    "company_id": self.company_id.id
                    }
            self.mrp_lot_id = self.env['stock.production.lot'].create(vals)
        return super(mrp_production_al,self).open_produce_product()


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    # @api.multi
    def set_lot_serial(self):
        self.ensure_one()
        index = 0
        print("==self.move_finished_ids==", self.move_finished_ids)
        print("==move_raw_ids==", self.move_raw_ids)
        print("==self.move_line_ids==", self.move_line_ids)
        for move_line in self.move_finished_ids:
            move_line.lot_id = self.move_line_ids[index].lot_id.id
            index += 1

    # @api.multi
    def button_start(self):
        self.ensure_one()
        res = super(MrpWorkorder,self).button_start()
        if not self.finished_lot_id and self.product_id.tracking == 'serial':
            lot_serial_type = self.env['ir.config_parameter'].sudo().get_param('mai_auto_lotserial_mrp_workorder.lot_serial_method')
            if lot_serial_type == 'production_date':
                date = self.production_date.strftime('%Y%m%d')
            else:
                date = datetime.now().strftime('%Y%m%d')
            counter = 1
            lot_id_name = date
            lot_ids = self.env['stock.production.lot'].search([('name',"ilike",date)])
            if lot_ids:
                counter = len(lot_ids) + 1
            lot_id_name = date + "000" + str(counter)
            vals = {
                    "product_id":self.product_id.id,
                    "name":lot_id_name,
                    "company_id": self.company_id.id
                    }
            self.finished_lot_id = self.env['stock.production.lot'].create(vals)
        # self.set_lot_serial()
        return res

    # @api.multi
    def record_production(self):
        if not self.finished_lot_id and self.product_id.tracking == 'serial':
            lot_serial_type = self.env['ir.config_parameter'].sudo().get_param('mai_auto_lotserial_mrp_workorder.lot_serial_method')
            if lot_serial_type == 'production_date':
                date = self.production_date.strftime('%Y%m%d')
            else:
                date = datetime.now().strftime('%Y%m%d')
            counter = 1
            lot_id_name = date
            lot_ids = self.env['stock.production.lot'].search([('name',"ilike",date)])
            if lot_ids:
                counter = len(lot_ids) + 1
            lot_id_name = date + "000" + str(counter)
            vals = {
                    "product_id":self.product_id.id,
                    "name":lot_id_name,
                    "company_id": self.company_id.id
                    }
            self.finished_lot_id = self.env['stock.production.lot'].create(vals)
        # self.set_lot_serial()
        return super(MrpWorkorder,self).record_production()