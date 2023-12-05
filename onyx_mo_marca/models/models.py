# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID,_


class MrpMarca(models.Model):
    _name = 'mrp.marca'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    name = fields.Char('Referencia')
    line_ids = fields.One2many('mrp.marca.line', 'marca_id', readonly=False, string='Marca Lines')
    mo_ids = fields.One2many('mrp.production', 'marca_id', domain=[('state','in',('confirmed','progress','to_close'))], string='MO')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('closed', 'Closed'),
            ('processed', 'Processed'),
            ('finish', 'Finished'),
        ],
        string='State', required=True,
        default='draft')
    
    def action_marca_close(self):
        return self.write({'state': 'closed'})
    
    def action_marca_read_consumption(self):
        for mo in self.mo_ids:
            for mp in mo.move_raw_ids:
                domain = [('product_id', '=', mp.product_id.id),('marca_id', '=', self.id)]
                line = self.line_ids.search(domain)
                if line:
                    line.planned_consumption += mp.product_uom_qty
                    line.manufacture_qty += mo.product_qty
                else:
                    dict = {
                        'product_id': mp.product_id.id,
                        'manufacture_qty': mo.product_qty,
                        'planned_consumption': mp.product_uom_qty,
                        'marca_id': self.id,
                    }
                    self.line_ids.create(dict)
        return self.write({'state': 'processed'})
    
    def action_marca_real_consumption(self):
        print("|amrc||amrc||amrc||amrc||amrc||amrc||amrc||amrc||amrc||amrc||amrc||amrc||amrc||amrc||amrc||amrc||amrc|")
        for line in self.line_ids:
            print ("|amrc|line: ", line)
            product = line.product_id
            print ("|amrc|product: ", product, " " ,product.name)
            lotes = line.consumption_ids 
            for consumption in lotes:
                for mo in self.mo_ids:
                    domain = [('bom_id', '=', mo.bom_id.id),('product_id', '=', product.id)]
                    on_bom = self.env['mrp.bom.line'].search(domain)
                    print ("|amrc|mo.name: ", mo.product_id.name)
                    print ("|amrc|on_bom: ", on_bom)
                    if on_bom:
                        factor = on_bom.product_qty / line.planned_consumption
                        if len(lotes) == 1:
                            real_consumption = consumption.product_qty * factor
                        elif len(lotes) > 1:
                            real_consumption = consumption.product_qty * factor
                        domain = [('raw_material_production_id', '=', mo.id),('product_id', '=', product.id)]
                        move = self.env['stock.move'].search(domain)
                        if move:
                            vals={
                                'product_id': product.id,
                                'location_id': move.location_id.id,
                                'location_dest_id': move.location_dest_id.id,
                                'product_uom_id': move.product_uom.id,
                                'picking_id': move.picking_id.id,
                                'move_id': move.id,
                                'qty_done':real_consumption,
                                }
                            if consumption.lot_id:
                                vals['lot_id'] = consumption.lot_id.id 
                            self.env['stock.move.line'].create(vals)
#                        total_consumption = real_consumption * mo.product_qty
                    #move.write({'product_uom_qty': total_consumption})
        return self.write({'state': 'finish'})
#        return False

    
class MrpMarcaLine(models.Model):
    _name = 'mrp.marca.line'
            
    marca_id = fields.Many2one('mrp.marca', string='Marca')
    consumption_ids = fields.One2many('mrp.marca.line.consumption', 'line_id', readonly=False, string='Line Consumptions')
    product_id = fields.Many2one(
        'product.product', 'Product',
        readonly=True, required=True,)
    manufacture_qty = fields.Float('Number of Finished Product to be Produced with this Raw Item')
    planned_consumption = fields.Float('Consumption Planned')
    real_consumption = fields.Float('Real Consumption', compute='action_marca_real_consumption')
    
    def action_marca_real_consumption(self):
        for reg in self:
            qty = 0
            for consumption in reg.consumption_ids:
                qty += consumption.product_qty
            reg.real_consumption = qty
            
    def action_show_details(self):
        self.ensure_one()

        view = self.env.ref('onyx_mo_marca.view_marca_line_consumptions_form')
        
        return {
            'name': _('Detailed Consumptions'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mrp.marca.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            'context': dict(
                self.env.context
            ),
        }
    
class MrpMarcaLineConsuptions(models.Model):
    _name = 'mrp.marca.line.consumption'
            
    line_id = fields.Many2one('mrp.marca.line', string='Marca Lines')
    product_id = fields.Many2one(
        'product.product', 'Product',
        required=True)
    product_qty = fields.Float('Real Consumption')
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id', '=', product_id)]", check_company=True)
    tracking = fields.Selection(related='product_id.tracking', required=True, readonly=True)
    
class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    marca_id = fields.Many2one('mrp.marca', string='Marca')