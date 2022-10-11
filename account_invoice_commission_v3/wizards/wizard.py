from odoo import models, fields, _
from odoo.exceptions import UserError


class CommissionAccountMove(models.TransientModel):
    _name = "commission.account.move"
    _description = "Commission Account Move"

    def generate_commissions(self):
        if self._context.get('active_model') == 'account.move':
            domain = [('id', 'in', self._context.get('active_ids', [])), ('commission_move_id', '=', False)]
        else:
            raise UserError(_("Missing 'active_model' in context."))

        moves = self.env['account.move'].search(domain).filtered('line_ids')
        if not moves:
            raise UserError(_('There are no journal items without commissions calculated.'))
        print (moves)
        for move in moves:
            move.calculate_commissions()
        return {'type': 'ir.actions.act_window_close'}
