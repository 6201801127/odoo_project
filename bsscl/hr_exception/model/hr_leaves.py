from odoo import api, models, fields,_
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date


class ExceptionRule(models.Model):
    _inherit = 'exception.rule'

    rule_group = fields.Selection(
        selection_add=[('hr_leave', 'Hr Leave'),
                       ],
    )
    model = fields.Selection(
        selection_add=[
            ('hr.leave', 'Hr Leave'),
        ])


class HrLeave(models.Model):
    _inherit = ['hr.leave', 'base.exception']
    _name = 'hr.leave'
    _order = 'main_exception_id asc,name desc'

    rule_group = fields.Selection(
        selection_add=[('hr_leave', 'Hr Leave')],
        default='hr_leave',
    )

    @api.model
    def test_all_draft_orders(self):
        order_set = self.search([('state', '=', 'confirm')])
        order_set.test_exceptions()
        return True

    # @api.constrains('ignore_exception','state')
    # def sale_check_exception(self):
    #     if self.state == 'validate':
    #         self._check_exception()

    def action_draft(self):
        res = super(HrLeave, self).action_draft()
        orders = self.filtered(lambda s: s.ignore_exception)
        orders.write({
            'ignore_exception': False,
        })
        return res

    def action_approve(self):
        if self.holiday_status_id.leave_type == 'Child Care Leave':
            today = date.today()
            if self.request_date_from < today or self.request_date_to < today:
                raise ValidationError(_('you are not allowed to approve this leave as the date selected are past date which are not allowed for CCL, please refuse the request and send back to employee.'))
        if self.detect_exceptions():
            return self._popup_exceptions()
        else:
            return super(HrLeave, self).action_approve()

    @api.model
    def _get_popup_action(self):
        action = self.env.ref('hr_exception.action_hr_leave_confirm')
        return action

    def action_refuse(self):
        exception = self.env['approvals.list'].search([('resource_ref', '=', 'hr.leave' + ',' + str(self.id)),
                                                       ('state', '=', 'pending_approval')])
        # print("------------------exception",exception)
        # (wagisha)commented to not show UserError
        # if exception:
        #     raise UserError(_('Do not allow Pending Approval Leave for Refuse.'))
        return super(HrLeave, self).action_refuse()

    def action_draft(self):
        exception = self.env['approvals.list'].search([('resource_ref', '=', 'hr.leave' + ',' + str(self.id)),
                                                       ('state', '=', 'pending_approval')])
        # print("------------------exception",exception)
        if exception:
            raise UserError(_('Do not allow Pending Approval Leave for Reset.'))
        return super(HrLeave, self).action_draft()


class Approvalslist(models.Model):
    _inherit = "approvals.list"

    def approve(self):
        res = super(Approvalslist, self).approve()
        if res:
            # print("----------------------self.model_id.model", self.model_id.model)
            if self.model_id.model == 'hr.leave':
                self.resource_ref.action_approve()
        return res

    def reject(self):
        res = super(Approvalslist, self).reject()
        if res:
            if self.model_id.model == 'hr.leave':
                self.resource_ref.action_refuse()
        return res

