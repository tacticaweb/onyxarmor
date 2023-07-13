# -*- coding: utf-8 -*-

import logging

from collections import OrderedDict

from odoo import api, fields, models, SUPERUSER_ID,_

import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def compute_item_name(self):
        def find(lst, key, value):
            for i, dic in enumerate(lst):
                if dic[key] == value:
                    return i
            return -1
    
        def definir_atributos(line):
            desc = ""
            atributos = line.product_id.product_template_attribute_value_ids
            for atributo in atributos:
                if atributo.attribute_id.name == "Front Size":
                    desc += " " + atributo.attribute_id.name + ":" + atributo.name 
                if atributo.attribute_id.name == "Back Size":
                    desc += " " + atributo.attribute_id.name + ":" + atributo.name
                if atributo.attribute_id.name == "Color":
                    desc += " " + atributo.attribute_id.name + ":" + atributo.name
            return desc
        
        interaccion = 0
        chaleco = 0
        items = []
        name = ""
        cantidad = 0
        price = 0
        ppal = ""
        
        for line in self.invoice_line_ids:
            if not line.psnum:
                atributos = definir_atributos(line)
                name = str(line.product_id.product_tmpl_id.name) + ' ' + atributos
                cantidad = line.quantity
                price = line.price_unit
                items.append({
                        'name': name,
                        'quantity': cantidad,
                        'price': round(price,2),
                        'taxes': line.tax_ids
                        })
            elif chaleco == 0:
                if line.product_id.product_tmpl_id.categ_id.principal:
                    atributos = definir_atributos(line)
                    ppal = str(line.product_id.product_tmpl_id.name) + ' ' + atributos
                    cantidad = line.quantity
                else:
                    name = str(line.product_id.product_tmpl_id.name)
                    cantidad = 1
                name = ppal + ' ' + name
                price = line.price_unit
                chaleco = line.psnum
            elif chaleco == line.psnum:
                if line.product_id.product_tmpl_id.categ_id.principal:
                    atributos = definir_atributos(line)
                    ppal = str(line.product_id.product_tmpl_id.name) + ' ' + atributos
                else:
                    name = str(line.product_id.product_tmpl_id.name)
                name = ppal + name
                price += line.price_unit
            elif chaleco != line.psnum and chaleco != 0:
                index = find(items,'name',name)
                if index > -1:
                    items[index]['quantity'] += cantidad 
                else:
                    items.append({
                        'name': name,
                        'quantity': cantidad,
                        'price': round(price,2),
                        'taxes': line.tax_ids
                        })
                ppal = ""
                name = ""
                if line.product_id.product_tmpl_id.categ_id.principal or not line.psnum:
                    atributos = definir_atributos(line)
                    ppal = str(line.product_id.product_tmpl_id.name) + ' ' + atributos
                    cantidad = line.quantity
                else:
                    name = str(line.product_id.product_tmpl_id.name)
                    cantidad = 1
                name = ppal + name
                price = line.price_unit
                chaleco = line.psnum
            if line == self.invoice_line_ids[-1]:
                items.append({
                        'name': name,
                        'quantity': cantidad,
                        'price': round(price,2),
                        'taxes': line.tax_ids
                        })
            dictionary = []
        for item in items:
            dictionary.append(item)
        return dictionary
                
            

class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    principal = fields.Boolean(string='Categoria Principal')