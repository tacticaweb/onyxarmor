# -*- coding: utf-8 -*-

import logging
import werkzeug

from collections import namedtuple, OrderedDict, defaultdict
from odoo import api, fields, models, _
from odoo import http, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round, float_is_zero
import datetime
import pytz

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_agency = fields.Boolean(string='Is an Agency')
    cod_logistic_operator = fields.Char(string='Cod Logistic Operator')
    logistic_operator_name = fields.Char(string='Logistic Operator Name')
    sizes = fields.One2many('res.sizing', 'agent', string="Agency")

class ResSizing(models.Model):
    _name = 'res.sizing'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    name = fields.Char(string='Sizing', compute='_compute_name')
    agency = fields.Many2one('res.partner', string="Agency")
    agent = fields.Many2one('res.partner', string="Officer")
    sale_representative = fields.Many2one('res.users', string="Sale Representative")
    date = fields.Date(string='Date', default=fields.Date.today())
    height_ft = fields.Float(string='Height Ft')
    height_in = fields.Float(string='Height Inches')
    weight = fields.Float(string='Weight')
    chest_measure = fields.Float(string='Chest')
    abdomen_measure = fields.Float(string='Abdomen')
    length_front_measure = fields.Float(string='Length Front')
    length_back_measure = fields.Float(string='Length Back')
    inf_vest_model = fields.Char(string='Length Back')
    inf_color = fields.Char(string='Color')
    inf_duty_belt_on = fields.Boolean(string='Duty Belt On')
    inf_duty_pant_on = fields.Boolean(string='Length Back')
    inf_overlap = fields.Selection([
            ('1', '1 Inch (Each Side)'),
            ('2', '2 Inches (Each Side)'),
            ('0', 'BUT FIT'),
        ],
        string='Overlap', required=True,
        default='1')
    size_front = fields.Selection([
            ('XS', 'XS'),
            ('SM', 'SM'),
            ('MD', 'MD'),
            ('LG', 'LG'),
            ('XL', 'XL'),
            ('2XL', '2XL'),
            ('3XL', '3XL'),
            ('4XL', '4XL'),
            ('5XL', '5XL'),
            ('6XL', '6XL'),
        ],
        string='Size Front', required=True,
        default='MD')
    size_front_length = fields.Selection([
            ('-2 inch', '-2 inch'),
            ('-1 inch', '-1 inch'),
            ('0 inch', '0 inch'),
            ('+1 inch', '+1 inch'),
            ('+2 inch', '+2 inch'),
            ('+3 inch', '+3 inch'),
            ('+4 inch', '+4 inch'),
            ('+5 inch', '+5 inch'),
            ('+6 inch', '+6 inch'),
            ],
        string='Size Front Length', required=True,
        default='0 inch')
    size_width = fields.Selection([
            ('-2 inch', '-2 inch'),
            ('-1 inch', '-1 inch'),
            ('0 inch', '0 inch'),
            ('+1 inch', '+1 inch'),
            ('+2 inch', '+2 inch'),
            ('+3 inch', '+3 inch'),
            ('+4 inch', '+4 inch'),
            ('+5 inch', '+5 inch'),
            ('+6 inch', '+6 inch'),            ],
        string='Size Width', required=True,
        default='0 inch')
    size_back = fields.Selection([
            ('XS', 'XS'),
            ('SM', 'SM'),
            ('MD', 'MD'),
            ('LG', 'LG'),
            ('XL', 'XL'),
            ('2XL', '2XL'),
            ('3XL', '3XL'),
            ('4XL', '4XL'),
            ('5XL', '5XL'),
            ('6XL', '6XL'),
        ],
        string='Size Back', required=True,
        default='MD')
    size_back_length = fields.Selection([
            ('-2 inch', '-2 inch'),
            ('-1 inch', '-1 inch'),
            ('0 inch', '0 inch'),
            ('+1 inch', '+1 inch'),
            ('+2 inch', '+2 inch'),
            ('+3 inch', '+3 inch'),
            ('+4 inch', '+4 inch'),
            ('+5 inch', '+5 inch'),
            ('+6 inch', '+6 inch'),
            ],
        string='Size Back Length', required=True,
        default='0 inch')
    deviations = fields.Text(string='Deviations requested by officer')
    additional_notes = fields.Text(string='Additional Notes')
    signature = fields.Binary(string='Officer Signature')
    
    
    @api.depends('agency', 'agent', 'date')
    def _compute_name(self):
        for test in self:
            test.name = str(test.agent.name) + ' ' + str(test.agency.name) + ' ' + str(test.date) 
            
    def write(self, vals):
        tallaje = ""
        if 'size_front' in vals:
            tallaje = tallaje + str(vals['size_front'])
        else:
            tallaje = tallaje + str(self.size_front)
        if 'size_front_length' in vals:
            tallaje = tallaje + str(vals['size_front_length'])
        else:
            tallaje = tallaje + str(self.size_front_length)
        if 'size_width' in vals:
            tallaje = tallaje + str(vals['size_width'])
        else:
            tallaje = tallaje + str(self.size_width)
        if 'size_back' in vals:
            tallaje = tallaje + str(vals['size_back'])
        else:
            tallaje = tallaje + str(self.size_back)
        if 'size_back_length' in vals:
            tallaje = tallaje + str(vals['size_back_length'])
        else:
            tallaje = tallaje + str(self.size_back_length)
        message = "Tallaje modificado con el siguiente codigo:" + (str(tallaje))
        self.message_post(body=message)
        res = super(ResSizing,self).write(vals)
        return res
    
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    #agent = fields.Many2one('res.partner', string="Officer", domain="[('is_agency','=',False)]")
    psnum = fields.Char(string='PSNUM')
        
    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'name': self.name,
            #'agent': self.agent,
            'psnum': self.psnum,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if self.display_type:
            res['account_id'] = False
        return res
        
    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        print ("_action_launch_stock_rule")
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        procurements = []
        for line in self:
            if line.state != 'sale' or not line.product_id.type in ('consu','product'):
                continue
            qty = line._get_qty_procurement(previous_product_uom_qty)
            if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
                continue

            group_id = line._get_procurement_group()
            if not group_id:
                group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
                line.order_id.procurement_group_id = group_id
            else:
                # In case the procurement group is already created and the order was
                # cancelled, we need to update certain values of the group.
                updated_vals = {}
                if group_id.partner_id != line.order_id.partner_shipping_id:
                    updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
                if group_id.move_type != line.order_id.picking_policy:
                    updated_vals.update({'move_type': line.order_id.picking_policy})
                if updated_vals:
                    group_id.write(updated_vals)

            values = line._prepare_procurement_values(group_id=group_id)
            product_qty = line.product_uom_qty - qty

            line_uom = line.product_uom
            quant_uom = line.product_id.uom_id
            product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
            line_name = str(line.product_id.name)
            procurements.append(self.env['procurement.group'].Procurement(
                line.product_id, product_qty, procurement_uom,
                line.order_id.partner_shipping_id.property_stock_customer,
                line_name, line.order_id.name, line.order_id.company_id, values))
        if procurements:
            print ("procurements: ", procurements)
            self.env['procurement.group'].run(procurements)
        return True
        
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    #agent = fields.Many2one('res.partner', string="Officer", domain="[('is_agency','=',False)]")
    psnum = fields.Char(string='PSNUM')
        
class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'
    
    @api.model
    def run(self, procurements, raise_user_error=True):
        """ Method used in a procurement case. The purpose is to supply the
        product passed as argument in the location also given as an argument.
        In order to be able to find a suitable location that provide the product
        it will search among stock.rule.
        """
        actions_to_run = defaultdict(list)
        errors = []
        for procurement in procurements:
            procurement.values.setdefault('company_id', procurement.location_id.company_id)
            procurement.values.setdefault('priority', '1')
            procurement.values.setdefault('date_planned', fields.Datetime.now())
            if (
                procurement.product_id.type not in ('consu', 'product') or
                float_is_zero(procurement.product_qty, precision_rounding=procurement.product_uom.rounding)
            ):
                continue
            rule = self._get_rule(procurement.product_id, procurement.location_id, procurement.values)
            
            print ("rule: ", rule)
            if not rule:
                errors.append(_('No rule has been found to replenish "%s" in "%s".\nVerify the routes configuration on the product.') %
                    (procurement.product_id.display_name, procurement.location_id.display_name))
            else:
                action = 'pull' if rule.action == 'pull_push' else rule.action
                actions_to_run[action].append((procurement, rule))
                print ("actions_to_run: ", actions_to_run)

        if errors:
            raise UserError('\n'.join(errors))

        for action, procurements in actions_to_run.items():
            if hasattr(self.env['stock.rule'], '_run_%s' % action):
                try:
                    getattr(self.env['stock.rule'], '_run_%s' % action)(procurements)
                except UserError as e:
                    errors.append(e.name)
            else:
                _logger.error("The method _run_%s doesn't exist on the procurement rules" % action)

        if errors:
            raise UserError('\n'.join(errors))
        return True
    
class StockRule(models.Model):
    _inherit = 'stock.rule'
    
    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        group_id = False
        if self.group_propagation_option == 'propagate':
            group_id = values.get('group_id', False) and values['group_id'].id
        elif self.group_propagation_option == 'fixed':
            group_id = self.group_id.id

        date_expected = fields.Datetime.to_string(
            fields.Datetime.from_string(values['date_planned']) - relativedelta(days=self.delay or 0)
        )

        partner = self.partner_address_id or (values.get('group_id', False) and values['group_id'].partner_id)
        if partner:
            product_id = product_id.with_context(lang=partner.lang or self.env.user.lang)

        # it is possible that we've already got some move done, so check for the done qty and create
        # a new move with the correct qty
        qty_left = product_qty
        move_values = {
            'name': name[:2000],
            'company_id': self.company_id.id or self.location_src_id.company_id.id or self.location_id.company_id.id or company_id.id,
            'product_id': product_id.id,
            'product_uom': product_uom.id,
            'product_uom_qty': qty_left,
            'partner_id': partner.id if partner else False,
            'location_id': self.location_src_id.id,
            'location_dest_id': location_id.id,
            'move_dest_ids': values.get('move_dest_ids', False) and [(4, x.id) for x in values['move_dest_ids']] or [],
            'rule_id': self.id,
            'procure_method': self.procure_method,
            'origin': origin,
            'picking_type_id': self.picking_type_id.id,
            'group_id': group_id,
            'route_ids': [(4, route.id) for route in values.get('route_ids', [])],
            'warehouse_id': self.propagate_warehouse_id.id or self.warehouse_id.id,
            'date': date_expected,
            'propagate_cancel': self.propagate_cancel,
            'description_picking': name,
            'priority': values.get('priority', "1"),
        }
        for field in self._get_custom_move_fields():
            if field in values:
                move_values[field] = values.get(field)
        return move_values