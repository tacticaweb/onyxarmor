# Copyright 2015-2021 Soluciones Opensource - Luis Miguel Varón E
# Copyright 20121 Soluciones Opensource - Luis Miguel Varón E
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountMove(models.Model):
    """Add some fields related to commissions"""

    _inherit = "account.move"
    
    commission_move_id = fields.Many2one('account.move', 'Commission Entry', readonly=True, copy=False)
    reference_partner = fields.Many2one('res.partner', string="Salesman or Reference", domain="[('agent','=',True)]", required=True)
    
    def calculate_commissions(self):
        new_lines = []
        if not self.commission_move_id:
            sale_person = self.reference_partner
            if sale_person.commission_id:
                commission = sale_person.commission_id
                move_dict = {
                    'narration': 'Commission Invoice %s' %(self.name),
                    'ref': self.invoice_date.strftime('%B %Y'),
                    'journal_id': commission.journal_id.id,
                    'date': self.invoice_date,
                    'move_type':'entry'
                }
                if self.move_type == 'out_refund':
                    account_debit = commission.account_credit.id
                    account_credit = commission.account_debit.id
                else:
                    account_debit = commission.account_debit.id
                    account_credit = commission.account_credit.id
                porcentage= commission.fix_qty
                value_commission = self.amount_total * (porcentage / 100)
                debit = {
                        'name': 'Cost Commission Invoice %s' %(self.name),
                        'move_id': self.id,
                        'account_id': account_debit,
                        'partner_id': sale_person.id,
                        'move_id': self.id,
                        'debit': value_commission,
                        'credit': 0,
                        'date': self.invoice_date,
                        'journal_id': commission.journal_id.id
                }
                new_lines.append(debit)
                credit = {
                        'name': 'Payable Commission for Invoice %s' %(self.name),
                        'move_id': self.id,
                        'account_id': account_credit,
                        'partner_id': sale_person.id,
                        'move_id': self.id,
                        'debit': 0,
                        'credit': value_commission,
                        'date': self.invoice_date,
                        'journal_id': commission.journal_id.id
                }
                new_lines.append(credit)
                if sale_person.supervisor_id:
                    commission = sale_person.supervisor_id.commission_id
                    porcentage= commission.fix_qty
                    value_commission = self.amount_total * (porcentage / 100)
                    if self.move_type == 'out_refund':
                        account_debit = commission.account_credit.id
                        account_credit = commission.account_debit.id
                    else:
                        account_debit = commission.account_debit.id
                        account_credit = commission.account_credit.id
                    debit = {
                        'name': 'Cost Supervisor Commission Invoice %s' %(self.name),
                        'move_id': self.id,
                        'account_id': account_debit,
                        'partner_id': sale_person.supervisor_id.id,
                        'move_id': self.id,
                        'debit': value_commission,
                        'credit': 0,
                        'date': self.invoice_date,
                        'journal_id': commission.journal_id.id
                    }
                    new_lines.append(debit)
                    credit = {
                        'name': 'Payable Supervisor Commission for Invoice %s' %(self.name),
                        'move_id': self.id,
                        'account_id': account_credit,
                        'partner_id': sale_person.supervisor_id.id,
                        'move_id': self.id,
                        'debit': 0,
                        'credit': value_commission,
                        'date': self.invoice_date,
                        'journal_id': commission.journal_id.id
                    }
                    new_lines.append(credit)
                    
                move_dict['line_ids'] = [(0, 0, line_vals) for line_vals in new_lines]
                move = self._create_account_move(move_dict)
                self.write({'commission_move_id': move.id})
                move.action_post()
            else:
                print ("Sale Person without commissions configured")
        else:
            print ("Commission Already Calculated")
        return 1
    
    def _create_account_move(self, values):
        return self.env['account.move'].create(values)
    
    def action_post(self):
        self._post(soft=False)
        if (self.move_type == 'out_invoice' or self.move_type == 'out_refund') and not self.reference_partner:
            print ("not self.reference_partner")
            self.reference_partner = self.invoice_user_id.partner_id.id
            print ("self.reference_partner: ",self.reference_partner)
        return True
        
        
