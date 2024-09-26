from odoo import models, fields, api


class kw_adv_apply_claim_wizard(models.TransientModel):
    _name = 'kw_advance_apply_claim_wizard'
    _description = 'Apply Claim Settlement Wizard'

    forwardto_id = fields.Many2one('hr.employee', string="Forward To",required=True)
    remark = fields.Text(string="remark",required=True)
    claim_record_id = fields.Many2one('kw_advance_claim_settlement',string="Ref")
    
    
    def claim_fwd_take_action_btn(self):
        if self.claim_record_id.state in ['applied','forward']:
            self.claim_record_id.write({
                'state': 'forward',
                'ra_remark': self.remark,
                'action_to_be_taken_by': self.forwardto_id.id,
                'forwarded_by': self.env.user.employee_ids.id,
                })

            # self.env.user.notify_success("Forwarded successfully")
            #Log
            record = self.env['kw_advance_log_claim_settlement'].create({
                'from_user_id':self._uid,
                'forwarded_to_user_id':self.forwardto_id.user_id.id,
                'remark':self.remark
                })
            forwardto_email = self.forwardto_id.work_email
            forwardto_name = self.forwardto_id.name
            mail_context = 'Forwarded'
            claim_category_list = []
            claim_type_list = []
            for record in self.claim_record_id.claim_bill_line_ids:
                claim_category_list.append(record.category_id.name)
                claim_type_list.append(record.claim_type_id.claim_type  if record.claim_type_id else '')
            claim_category = ','.join(claim_category_list) 
            claim_type =  ','.join(claim_type_list)
            template_id = self.env.ref('kw_advance_claim.kw_claim_settlement_forward_mail_template')
            template_id.with_context(status=mail_context,mail=forwardto_email,name=forwardto_name,claim_category=claim_category,claim_type=claim_type).send_mail(self.claim_record_id.id, notif_layout="kwantify_theme.csm_mail_notification_light")
            user_template_id = self.env.ref('kw_advance_claim.kw_claim_settlement_user_forward_mail_template')
            user_template_id.with_context(
                status=mail_context,
                claim_category=claim_category,
                claim_type=claim_type,
                fname=self.forwardto_id.name).send_mail(self.claim_record_id.id, notif_layout="kwantify_theme.csm_mail_notification_light")
        return {'type': 'ir.actions.act_window_close'}
    
    @api.onchange('forwardto_id')
    def get_forwardto_id(self):
        fwd_lst = []
        login_user_id = self.env.user.employee_ids.id
        ra_group = self.env.ref('bsscl_employee.group_hr_ra')
        ra_employee_ids = ra_group.users.mapped('employee_ids') or False
        if ra_employee_ids:
            for rec in ra_employee_ids:
                fwd_lst.append(rec.id)
        fwd_lst.remove(login_user_id)
        return {'domain': {'forwardto_id': [('id', 'in', fwd_lst)]}}
