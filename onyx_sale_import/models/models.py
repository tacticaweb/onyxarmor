  # -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import pytz
import time
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import xlrd
import tempfile
import binascii

class ImportSale(models.Model):
    _name = 'import.sale'
    _description = 'Import Sale Order Lines'
    _inherit = ['mail.thread']

    import_doc = fields.Integer(string='N° de Documento', readonly=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    excel_file = fields.Binary(string='Excel File') 
    state = fields.Selection([
        ('draft', 'Draft'),
        ('readed', 'Imported'),
        ('validated', 'Validated'),
        ('complete', 'Complete'),
    ], string='State', index=True, readonly=True, copy=False, default='draft')
    import_sale_lines = fields.One2many('import.sale.lines','import_id', string='Import Line Dteail')
    
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('import.sale') or '/'
        vals['import_doc'] = seq
        return super(ImportSale, self).create(vals)
    
    def name_get(self):
        result = []
        for s in self:
            name = 'Import #' + str(s.import_doc)
            result.append((s.id, name))
        return result
    
    def read_file(self):
        import_lines = self.env['import.sale.lines']
        
        if self.excel_file is None:
            return self.write({'state': 'readed'})
        else:
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.excel_file))
            fp.seek(0)
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            for row_no in range(sheet.nrows):
                print ("row_no: ",row_no)
                color = ""
                carrier = ""
                if row_no <= 0:
                    fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    line = list(map(lambda row:isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    print("************PSNUM  ********************", type(line[0]), line[0])
                    print("************TEMPLATE ID ********************", type(line[1]), line[1])
                    print("************SIZING  ********************", type(line[2]), line[2])
                    print("************QUANTITY  ********************", type(line[3]), line[3])
                    print("************COLOR  ********************", type(line[4]), line[4])
                    print("************CARRIER  ********************", type(line[5]), line[5])
                    
                    if line[4]:
                        color = str(line[4]).split("'")[1]
                    if line[5]:
                        carrier = str(line[5]).split("'")[1]
                    
                    
                    import_lines.create({
                        'psnum': int(str(line[0]).split('.')[0]),
                        'product_template_id': int(str(line[1]).split('.')[0]),
                        'sizing_id': int(str(line[2]).split('.')[0]),
                        'quantity': int(str(line[3]).split('.')[0]),
                        'color': color,
                        'carrier': carrier,
                        'import_id': self.id
                    })  
                    print("Datos guardados:")
                    for i, item in enumerate(line):
                        print(f"{i}. {item} ({type(item)})")
                    print ("==========",line)  
            return self.write({'state': 'readed'})
                
    
    def validate_info(self):
        
        for line in self.import_sale_lines:
            variant = []
            for attribute_line in line.product_template_id.attribute_line_ids.attribute_id:
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
            print ("product: ",product)
            if self.psnum:
                psnum = self.psnum
            else:
                psnum = 0
                
            if len(str(product.display_name).split("(")) > 2:
                name = str(product.display_name).split("(")[0] + str(product.display_name).split("(")[1] + ")" 
            else:
                name = str(product.display_name)    
            
            order_line_data = {
                    'order_id': self.sale_order_id.id,
                    'name': str(product.display_name) + ' Agent: ' + str(self.agent.name),
                    'psnum': psnum,
                    'size': self.sizes.id,
                    'product_id': product.id,
                    'price_unit': product.lst_price,
                    'product_uom_qty': 1
                }
            
            print ("order_line_data: ",order_line_data)
            order_line = self.env['sale.order.line'].create(order_line_data)
    
    
    
    def set_draft(self):
        return self.write({'state': 'draft'})
    
class ImportSaleLine(models.Model):
    _name = 'import.sale.lines'
    _description = 'Import Sale Detail'

    psnum = fields.Integer(string='PSNUM')
    product_template_id = fields.Many2one('product.template', string='Product Template')
    sizing_id = fields.Many2one('res.sizing', string='Sizing')
    quantity = fields.Integer(string='Quantity')
    color = fields.Char(string='Color')
    carrier = fields.Char(string='Carrier')
    product_id = fields.Many2one('product.product', string='Product')
    sale_order_line = fields.Many2one('sale.order.line', string='Sale Order Line')
    
    import_id = fields.Many2one('import.sale', string='Import Sale Order')
    
    
    def name_get(self):
        result = []
        for s in self:
            if s.product_id:
                name = str(s.id) + '-' + str(s.product_template_id.name) + '-' + str(s.sizing_id.agent.name)
            else:
                name = str(s.id) + '-' + str(s.product_id.name) + '-' + str(s.sizing_id.agent.name)
            result.append((s.id, name))
        return result
    
    
    