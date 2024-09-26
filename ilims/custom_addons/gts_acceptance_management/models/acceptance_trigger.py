# Copyright 2010 NaN Projectes de Programari Lliure, S.L.
# Copyright 2014 Serv. Tec. Avanzados - Pedro M. Baeza
# Copyright 2014 Oihane Crucelaegui - AvanzOSC
# Copyright 2017 ForgeFlow S.L.
# Copyright 2017 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AcceptanceTrigger(models.Model):
    _name = "acceptance.trigger"
    _description = "Acceptance Trigger"

    name = fields.Char(string="Name", required=True, translate=True)
    active = fields.Boolean(string="Active", default=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    partner_selectable = fields.Boolean(
        string="Selectable by partner",
        default=False,
        readonly=True,
        help="This technical field is to allow to filter by partner in triggers",
    )