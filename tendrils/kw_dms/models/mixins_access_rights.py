
import logging

from odoo import _
from odoo import models, api, fields
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)

class AccessModel(models.AbstractModel):
    
    _name = 'kw_dms_security.mixins.access_rights'
    _description = 'Access Mixin'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
            
    permission_read = fields.Boolean(
        compute='_compute_permissions_read',
        search='_search_permission_read',
        string="Read Access")
    
    permission_create = fields.Boolean(
        compute='_compute_permissions_create',
        search='_search_permission_create',
        string="Create Access")
    
    permission_write = fields.Boolean(
        compute='_compute_permissions_write',
        search='_search_permission_write',
        string="Write Access")
    
    permission_unlink = fields.Boolean(
        compute='_compute_permissions_unlink', 
        search='_search_permission_unlink',
        string="Delete Access")

    #----------------------------------------------------------
    # Search
    #----------------------------------------------------------
    
    @api.model
    def _search_permission_read(self, operator, operand):
        if operator == '=' and operand:
            return [('id', 'in', self.search([])._filter_access_ids('read'))]
        return [('id', 'not in', self.search([])._filter_access_ids('read'))]
    
    @api.model
    def _search_permission_create(self, operator, operand):
        if operator == '=' and operand:
            return [('id', 'in', self.search([])._filter_access_ids('create'))]
        return [('id', 'not in', self.search([])._filter_access_ids('create'))]
    
    @api.model
    def _search_permission_write(self, operator, operand):
        if operator == '=' and operand:
            return [('id', 'in', self.search([])._filter_access_ids('write'))]
        return [('id', 'not in', self.search([])._filter_access_ids('write'))]
    
    @api.model
    def _search_permission_unlink(self, operator, operand):
        if operator == '=' and operand:
            return [('id', 'in', self.search([])._filter_access_ids('unlink'))]
        return [('id', 'not in', self.search([])._filter_access_ids('unlink'))]

    #----------------------------------------------------------
    # Read, View 
    #----------------------------------------------------------
    
    @api.multi
    def _compute_permissions_read(self):
        records = self._filter_access('read')
        for record in records:
            record.update({'permission_read': True})
        for record in self - records:
            record.update({'permission_read': False})
            
    @api.multi
    def _compute_permissions_create(self):
        records = self._filter_access('create')
        for record in records:
            record.update({'permission_create': True})
        for record in self - records:
            record.update({'permission_create': False})
            
    @api.multi
    def _compute_permissions_write(self):
        records = self._filter_access('write')
        #print(records)
       
        for record in records:
            record.update({'permission_write': True})
        for record in self - records:
            record.update({'permission_write': False})
            
    @api.multi
    def _compute_permissions_unlink(self):
        records = self._filter_access('unlink')
        for record in records:
            record.update({'permission_unlink': True})
        for record in self - records:
            record.update({'permission_unlink': False})