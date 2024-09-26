from odoo import models, fields

class ApplyGrievanceLog(models.Model):
    _name           = 'kw_apply_grievance_action_log'
    _description    = "Apply Grievance Action Logs"

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    apply_grievance_id   = fields.Many2one('kw.grievance','Apply Grievance',required=True,ondelete="cascade")

    employee_id     = fields.Many2one('hr.employee',"Action Taken By",
                                  default=_default_employee, ondelete='restrict', index=True)
    date            = fields.Date(string='Date',default=fields.Date.context_today,required=True)
    state           = fields.Char("State",required=True)
    remark          = fields.Text("Remark",required=True)