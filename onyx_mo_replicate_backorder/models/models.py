# -*- coding: utf-8 -*-

import math
import re

from odoo import api, fields, models, SUPERUSER_ID,_
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero, float_repr, float_round

SIZE_BACK_ORDER_NUMERING = 3

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    def replicate_backorders(self):
        print("|rb||rb||rb||rb||rb||rb||rb||rb||rb||rb||rb||rb||rb||rb||rb||rb|Entró replicate_backorders")
        for reg in self:
            print("|rb|reg.product_qty: ", reg.product_qty)
            print("|rb|reg.product_id.tracking: ", reg.product_id.tracking)
            if reg.product_qty > 1 and reg.product_id.tracking == 'serial':
                for i in range(1, int(reg.product_qty)):
                    reg._generate_production_mo(i)
                    print("|rb| product_qty: ", reg.product_qty)
                    print("|rb| i: ", i)
                
    def _generate_production_mo(self, index):
        print("|gpm| Entró _generate_production_mo: ", index)
        productions = self.env['mrp.production']
        for production in self:
#            print ("Pre production.backorder_sequence: ",production.backorder_sequence)
#            if production.backorder_sequence == 0:
#                production.backorder_sequence = 1
#            print ("Post production.backorder_sequence: ",production.backorder_sequence)
            new_production = production.copy(default=production._get_production_mo_values(index + 1))
            print("|gpm| new_productiono: ", new_production)
            new_moves_vals = []
            for move in production.move_raw_ids | production.move_finished_ids:
                qty_to_split = move.unit_factor
                move_vals = move._split_mov(qty_to_split)
                if move.raw_material_production_id:
                    move_vals[0]['raw_material_production_id'] = new_production.id
                else:
                    move_vals[0]['production_id'] = new_production.id
                
                new_moves_vals.append(move_vals[0])
                move.product_uom_qty = move.product_uom_qty - move.unit_factor
            
            new_moves = self.env['stock.move'].create(new_moves_vals)
            productions |= new_production
            for old_wo, wo in zip(production.workorder_ids, new_production.workorder_ids):
                wo.qty_produced = max(old_wo.qty_produced - old_wo.qty_producing, 0)
                if wo.product_tracking == 'serial':
                    wo.qty_producing = 1
                else:
                    wo.qty_producing = wo.qty_remaining
                if wo.qty_producing == 0:
                    wo.action_cancel()

            production.name = self._get_name_backorder(production.name, 1)
            print ("|gpm|production.name: ",production.name)
            print ("|gpm|new_production.name: ",new_production.name)
            ratio = 1 / production.product_qty
            for workorder in production.workorder_ids:
                workorder.duration_expected = workorder.duration_expected * (1 - ratio)
            for workorder in new_production.workorder_ids:
                workorder.duration_expected = workorder.duration_expected * ratio
            production.product_qty = production.product_qty - 1
                
        self.move_raw_ids.filtered(lambda m: not m.additional)._do_unreserve()
        self.move_raw_ids.filtered(lambda m: not m.additional)._action_assign()
        
        productions.move_raw_ids.move_line_ids.filtered(lambda ml: ml.product_id.tracking == 'serial' and ml.product_qty == 0).unlink()
        productions.move_raw_ids._recompute_state()
        print ("|gpm|productions: ",productions)
        return productions
    
    def _get_production_mo_values(self, index):
        print("|gpmv| _get_production_mo_values: ", index)
        self.ensure_one()
        print("|gpmv| self._get_name_backorder(self.name, index): ", self._get_name_backorder(self.name, index))
        return {
            'name': self._get_name_backorder(self.name, index),
            'procurement_group_id': self.procurement_group_id.id,
            'move_raw_ids': None,
            'move_finished_ids': None,
            'product_qty': 1,
            'lot_producing_id': False,
            'origin': self.origin
        }
    
    def _pre_button_mark_done(self):
        print ("|pbmd||pbmd||pbmd||pbmd||pbmd||pbmd||pbmd||pbmd||pbmd||pbmd||pbmd|")
        productions_to_immediate = self._check_immediate()
        print ("|pbmd|productions_to_immediate: ",productions_to_immediate)
        if productions_to_immediate:
            return productions_to_immediate._action_generate_immediate_wizard()

        for production in self:
            print ("|pbmd|production: ",production)
            print ("|pbmd|float_is_zero(production.qty_producing, precision_rounding=production.product_uom_id.rounding)")
            print ("|pbmd|float_is_zero(%s, precision_rounding=%s)=%s" %(production.qty_producing,production.product_uom_id.rounding,float_is_zero(production.qty_producing, precision_rounding=production.product_uom_id.rounding)))
            if float_is_zero(production.qty_producing, precision_rounding=production.product_uom_id.rounding):
                print ("|pbmd|Entró Float_is_zero error quantity")
                raise UserError(_('The quantity to produce must be positive!'))

        consumption_issues = self._get_consumption_issues()
        if consumption_issues:
            return self._action_generate_consumption_wizard(consumption_issues)

        quantity_issues = self._get_quantity_produced_issues()
        if quantity_issues:
            return self._action_generate_backorder_wizard(quantity_issues)
        return True
    
    def button_mark_done(self):
        print ("|bmd||bmd||bmd||bmd||bmd||bmd||bmd||bmd||bmd||bmd||bmd|:", self)
        self._button_mark_done_sanity_checks()
        print ("|bmd|POS SANITY CHECK")
        if not self.env.context.get('button_mark_done_production_ids'):
            self = self.with_context(button_mark_done_production_ids=self.ids)
        print ("|bmd|PRE _pre_button_mark_done")
        res = self._pre_button_mark_done()
        print ("|bmd|POS _pre_button_mark_done: ", res)
        if res is not True:
            return res
        
        print ("|bmd|self.env.context.get('mo_ids_to_backorder'): ", self.env.context.get('mo_ids_to_backorder'))
        if self.env.context.get('mo_ids_to_backorder'):
            productions_to_backorder = self.browse(self.env.context['mo_ids_to_backorder'])
            print ("|bmd|productions_to_backorder:", productions_to_backorder)
            productions_not_to_backorder = self - productions_to_backorder
            print ("|bmd|productions_not_to_backorder:", productions_not_to_backorder)
        else:
            productions_not_to_backorder = self
            print ("|bmd|productions_not_to_backorder:", productions_not_to_backorder)
            productions_to_backorder = self.env['mrp.production']
            print ("|bmd|productions_to_backorder:", productions_to_backorder)

        print ("|bmd|PRE self.workorder_ids.button_finish()")
        self.workorder_ids.button_finish()
        print ("|bmd|POS self.workorder_ids.button_finish()")

        print ("|bmd|PRE productions_not_to_backorder._post_inventory(cancel_backorder=True)")
        productions_not_to_backorder._post_inventory(cancel_backorder=True)
        print ("|bmd|POS productions_not_to_backorder._post_inventory(cancel_backorder=True)")
        print ("|bmd|PRE productions_to_backorder._post_inventory(cancel_backorder=False)")
        productions_to_backorder._post_inventory(cancel_backorder=False)
        print ("|bmd|POS productions_to_backorder._post_inventory(cancel_backorder=False)")
        print ("|bmd|PRE backorders = productions_to_backorder._generate_backorder_productions()")
        backorders = productions_to_backorder._generate_backorder_productions()
        print ("|bmd|POS backorders = productions_to_backorder._generate_backorder_productions(): ", backorders)

        # if completed products make other confirmed/partially_available moves available, assign them
        print ("|bmd|PRE done_move_finished_ids = (productions_to_backorder.move_finished_ids | productions_not_to_backorder.move_finished_ids).filtered(lambda m: m.state == 'done')")
        done_move_finished_ids = (productions_to_backorder.move_finished_ids | productions_not_to_backorder.move_finished_ids).filtered(lambda m: m.state == 'done')
        print ("|bmd|POS done_move_finished_ids = (productions_to_backorder.move_finished_ids | productions_not_to_backorder.move_finished_ids).filtered(lambda m: m.state == 'done'): ", done_move_finished_ids)
        print ("|bmd|PRE done_move_finished_ids._trigger_assign()")
        done_move_finished_ids._trigger_assign()
        print ("|bmd|POS done_move_finished_ids._trigger_assign()")
        # Moves without quantity done are not posted => set them as done instead of canceling. In
        # case the user edits the MO later on and sets some consumed quantity on those, we do not
        # want the move lines to be canceled.
        (productions_not_to_backorder.move_raw_ids | productions_not_to_backorder.move_finished_ids).filtered(lambda x: x.state not in ('done', 'cancel')).write({
            'state': 'done',
            'product_uom_qty': 0.0,
        })

        print ("|bmd|PRE for production in self")
        for production in self:
            print ("|bmd|for production in self: ", production)
            print ("|bmd|production.qty_produced: ", production.qty_produced)
            production.write({
                'date_finished': fields.Datetime.now(),
                'product_qty': production.product_qty,
                'priority': '0',
                'is_locked': True,
            })
        print ("|bmd|POS for production in self")

        print ("|bmd|PRE for workorder in self.workorder_ids.filtered(lambda w: w.state not in ('done', 'cancel'))")
        for workorder in self.workorder_ids.filtered(lambda w: w.state not in ('done', 'cancel')):
            workorder.duration_expected = workorder._get_duration_expected()
        print ("|bmd|POS for workorder in self.workorder_ids.filtered(lambda w: w.state not in ('done', 'cancel'))")

        
        print ("|bmd|PRE if not backorders: ", backorders)
        if not backorders:
            print ("|bmd|ENTRÓ if not backorders")
            print ("|bmd|self.env.context.get('from_workorder'): ", self.env.context.get('from_workorder'))
            if self.env.context.get('from_workorder'):
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'mrp.production',
                    'views': [[self.env.ref('mrp.mrp_production_form_view').id, 'form']],
                    'res_id': self.id,
                    'target': 'main',
                }
            return True
        print ("|bmd|POS if not backorders: ", backorders)
        
        
        context = self.env.context.copy()
        context = {k: v for k, v in context.items() if not k.startswith('default_')}
        for k, v in context.items():
            if k.startswith('skip_'):
                context[k] = False
        action = {
            'res_model': 'mrp.production',
            'type': 'ir.actions.act_window',
            'context': dict(context, mo_ids_to_backorder=None)
        }
        print ("|bmd|POS context: ", context)
        
        print ("|bmd|PRE if len(backorders) == 1: ", len(backorders))
        if len(backorders) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': backorders[0].id,
            })
        else:
            action.update({
                'name': _("Backorder MO"),
                'domain': [('id', 'in', backorders.ids)],
                'view_mode': 'tree,form',
            })
        print ("|bmd|END action: ", action)
        return action
        
    @api.model
    def _get_name_backorder(self, name, sequence):
        if not sequence:
            return name
        seq_back = "-" + "0" * (SIZE_BACK_ORDER_NUMERING - 1 - int(math.log10(sequence))) + str(sequence)
        if re.search("-\\d{%d}$" % SIZE_BACK_ORDER_NUMERING, name):
            return name[:-SIZE_BACK_ORDER_NUMERING-1] + seq_back
        return name + seq_back
    
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    def _split_mov(self, qty, restrict_partner_id=False):
        self.ensure_one()
        
        defaults = self._prepare_move_split_values(qty)
        if restrict_partner_id:
            defaults['restrict_partner_id'] = restrict_partner_id

        if self.env.context.get('source_location_id'):
            defaults['location_id'] = self.env.context['source_location_id']
        new_move_vals = self.with_context(rounding_method='HALF-UP').copy_data(defaults)
        
        return new_move_vals
    
    def _prepare_move_split_values(self, qty):
        vals = {
            'product_uom_qty': qty,
            'procure_method': 'make_to_stock',
            'move_dest_ids': [(4, x.id) for x in self.move_dest_ids if x.state not in ('done', 'cancel')],
            'move_orig_ids': [(4, x.id) for x in self.move_orig_ids],
            'origin_returned_move_id': self.origin_returned_move_id.id,
            'price_unit': self.price_unit,
        }
        if self.env.context.get('force_split_uom_id'):
            vals['product_uom'] = self.env.context['force_split_uom_id']
        return vals
                