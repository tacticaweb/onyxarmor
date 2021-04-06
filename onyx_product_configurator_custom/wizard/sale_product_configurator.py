# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import itertools
from odoo import models, fields, api
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class OnyxProductConfigurator(models.TransientModel):
    _name = 'onyx.product.configurator'
    
    sale_order_id = fields.Many2one('sale.order', 'Order', readonly=True, default=lambda self: self.env.context.get('active_id'))
    agent = fields.Many2one('res.partner', string="Officer", domain="[('is_agency','=',False)]")
    sizes = fields.Many2one('res.sizing', string="Sizes", domain="[('agent','=',agent)]")
    psnum = fields.Integer(string="Set Number")
    product_tmpl_id = fields.Many2one('product.template',string="Product Template", domain="[('sizes_ok','=',True)]")
    products_ids = fields.Many2many('product.product', 'product_template_rel','id', 'products_templates', 'Products', domain="[('product_tmpl_id','in',[product_tmpl_id])]")
    product_attribute_ids = fields.Many2many('product.template.attribute.value', 'attribute_value_rel','id', 'products_templates_attribute_value', string="Attributes", domain="[('product_tmpl_id','in',[product_tmpl_id])]")
    
    def action_grabar(self):
        variant = []
        attribute = []
        for attribute_line in self.product_tmpl_id.attribute_line_ids.attribute_id:
            if attribute_line.name == "Front Size":
                for attribute_value in attribute_line.value_ids:
                    if attribute_value.name == self.sizes.size_front:
                        variant.append(attribute_value.id)
                        
            elif attribute_line.name == "Back Size":
                for attribute_value in attribute_line.value_ids:
                    if attribute_value.name == self.sizes.size_back:
                        variant.append(attribute_value.id)
                        
            elif attribute_line.name == "Width":
                for attribute_value in attribute_line.value_ids:
                    if attribute_value.name == self.sizes.size_width:
                        variant.append(attribute_value.id)
                        
            elif attribute_line.name == "Front Length":
                for attribute_value in attribute_line.value_ids:
                    if attribute_value.name == self.sizes.size_front_length:
                        variant.append(attribute_value.id)
                        
            elif attribute_line.name == "Back Length":
                for attribute_value in attribute_line.value_ids:
                    if attribute_value.name == self.sizes.size_back_length:
                        variant.append(attribute_value.id)
        combination = self.env['product.template.attribute.value'].search([('product_attribute_value_id','in',variant),('product_tmpl_id','=',self.product_tmpl_id.id)])    
        combination = combination | self.product_attribute_ids
        product = self.product_tmpl_id._create_product_variant(combination)
        if self.psnum:
            psnum = self.psnum
        else:
            psnum = 0
        
        order_line_data = {
                'order_id': self.sale_order_id.id,
                'name': product.display_name + ' Agent: ' + self.agent.name,
                'psnum': psnum,
                'product_id': product.id,
                'price_unit': product.lst_price,
                'product_uom_qty': 1
            }
        order_line = self.env['sale.order.line'].create(order_line_data)
          
        return True
        
        
        
