import os
import hashlib
import logging
import itertools

from odoo import _, SUPERUSER_ID
from odoo import models, api, fields
from odoo.exceptions import AccessError

from odoo.addons.kw_dms.tools.security import NoSecurityUid

_logger = logging.getLogger(__name__)

class LockingModel(models.AbstractModel):
    
    _name = 'kw_dms_security.mixins.locking'
    _description = 'Locking Mixin'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    locked_by = fields.Many2one(
        comodel_name='res.users',
        string="Locked by")
    
    is_locked = fields.Boolean(
        compute='_compute_locked',
        string="Locked")
    
    is_lock_editor = fields.Boolean(
        compute='_compute_locked', 
        string="Editor")
        
    #----------------------------------------------------------
    # Locking
    #----------------------------------------------------------

    @api.multi
    def lock(self):
        self.write({'locked_by': self.env.uid})
    
    @api.multi
    def unlock(self):
        self.write({'locked_by': None})

    @api.model
    def _check_lock_editor(self, lock_uid):
        return lock_uid in (self.env.uid, SUPERUSER_ID) or isinstance(self.env.uid, NoSecurityUid)
    
    @api.multi
    def check_lock(self):
        for record in self:
            if record.locked_by.exists() and not self._check_lock_editor(record.locked_by.id):
                message = _("The record (%s [%s]) is locked, by an other user.")
                # raise AccessError(message % (record._description, record.id)) 

    #----------------------------------------------------------
    # Read, View 
    #----------------------------------------------------------
    
    @api.depends('locked_by')
    def _compute_locked(self):
        for record in self:
            if record.locked_by.exists():
                record.update({'is_locked': True, 'is_lock_editor': record.locked_by.id == record.env.uid})
            else:
                record.update({'is_locked': False, 'is_lock_editor': False})

    #----------------------------------------------------------
    # Create, Update, Delete
    #----------------------------------------------------------

    @api.multi
    def _write(self, vals):
        self.check_lock()
        return super(LockingModel, self)._write(vals)


    @api.multi
    def unlink(self):  
        self.check_lock()
        return super(LockingModel, self).unlink()
    
