# -*- coding: utf-8 -*-

from odoo import models, fields, api

class kw_crm_tender_type_master(models.Model):
    _name       = 'kw_crm_tender_type_master'
    _description= 'Tender Type Master'
    _rec_name = 'name'

    name = fields.Char("Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    code = fields.Char("Code", required=True)
    sequence = fields.Integer(string="Sequence")                             
        