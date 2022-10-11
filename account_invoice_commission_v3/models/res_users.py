# Copyright 2015-2021 Soluciones Opensource - Luis Miguel Varón E
# Copyright 20121 Soluciones Opensource - Luis Miguel Varón E
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResPartners(models.Model):
    """Add some fields related to commissions"""

    _inherit = "res.partner"

    agent_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="partner_agent_rel",
        column1="partner_id",
        column2="agent_id",
        domain=[("agent", "=", True)],
        readonly=False,
        string="Agents",
    )
    # Fields for the partner when it acts as an agent
    agent = fields.Boolean(
        string="Earn Commission",
        help="Check this field if the user is a saleperson that earn Commission.",
    )
    supervisor_id = fields.Many2one('res.partner', string='Supervisor')
    commission_id = fields.Many2one(
        string="Commission",
        comodel_name="sale.commission",
        help="This is the default commission used in the sales where this "
        "agent is assigned. It can be changed on each operation if "
        "needed.",
    )
    

    @api.model
    def _commercial_fields(self):
        """Add agents to commercial fields that are synced from parent to childs."""
        res = super()._commercial_fields()
        res.append("agent_ids")
        return res
