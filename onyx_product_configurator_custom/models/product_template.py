from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
from mako.template import Template
from mako.runtime import Context
from odoo.tools.safe_eval import safe_eval
from io import StringIO
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sizes_ok= fields.Boolean(string="Use sizes")
    
    def toggle_sizes(self):
        for record in self:
            record.sizes_ok = not record.sizes_ok