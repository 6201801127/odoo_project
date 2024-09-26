# *******************************************************************************************************************
#  File Name             :   kw_specialization_master_sync.py
#  Description           :   This model is used to inherit stream master model and sync data into Kwantify 
#  Created by            :   Asish ku Nayak
#  Created On            :   10-08-2020
#  Modified by           :
#  Modified On           :
#  Modification History  :
# *******************************************************************************************************************


from odoo import models, fields, api
import json, requests


class kwmaster_specializations(models.Model):
    _inherit = 'kwmaster_specializations'

    sync_status = fields.Selection(
        string='Sync Status',
        selection=[('0', 'Not Required'), ('1', 'Pending'), ('2', 'Done')], compute='_check_sync_status')

    @api.multi
    def _check_sync_status(self):
        for record in self:
            log_record = self.env['kw_emp_sync_log'].sudo().search(
                ['&', ('model_id', '=', 'kwmaster_specializations'), ('rec_id', '=', record.id)])
            if log_record:
                status = log_record.mapped('status')
                if 0 in status:
                    record.sync_status = '1'
                else:
                    record.sync_status = '2'
            else:
                record.sync_status = '0'

    # For specialization Synchronization
    @api.model
    def action_sync_specialization(self):
        mail_id_rec = self.env['res.config.settings'].sudo().search([])
        last_mail_id = mail_id_rec[-1].kw_sync_error_log_mail if mail_id_rec else 'girish.mohanta@csm.tech'
        # Mail sent
        template_id = self.env.ref('kw_synchronization.kw_failed_api_template')

        specialization_rec = self.env['kw_emp_sync_log'].sudo().search(
            ['&', ('model_id', '=', 'kwmaster_specializations'), ('status', '=', 0)])
        specialization_sync = {}
        parameterurl = self.env['ir.config_parameter'].sudo().get_param('kw_employee_sync')
        specializationurl = parameterurl + 'AddSpecializationDetails'
        for rec in specialization_rec:
            specialization_record = self.env['kwmaster_specializations'].sudo().search([('id', '=', rec.rec_id)])
            specialization_sync['ActionCode'] = 'EQSPA' if specialization_record.kw_id == 0 else 'EQSPU'
            specialization_sync['SpecName'] = specialization_record.name
            specialization_sync['SpecId'] = str(specialization_record.kw_id)
            specialization_sync['StreamId'] = str(specialization_record.stream_id.kw_id)
            specialization_sync['CreatedBy'] = str(
                self.env['hr.employee'].sudo().search([('user_id', '=', specialization_record.create_uid.id)]).kw_id)
            specialization_sync['UpdatedBy'] = str(
                self.env['hr.employee'].sudo().search([('user_id', '=', specialization_record.create_uid.id)]).kw_id)

            header = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            resp = requests.post(specializationurl, headers=header, data=json.dumps(specialization_sync))

            j_data = json.dumps(resp.json())
            json_record = json.loads(j_data)

            if specialization_sync['ActionCode'] == 'EQSPA':
                if resp.status_code == 200:
                    if json_record['status'] == 1:
                        specialization_record.write({'kw_id': int(json_record['id'])})
                        rec.write({
                            'json_data': specialization_sync,
                            'status': 1,
                            'response_result': resp.json()})
                        self.env['kw_kwantify_integration_log'].sudo().create(
                            {'name': 'Specialization Master Sync Data',
                             'new_record_log': specialization_sync,
                             'request_params': specializationurl,
                             'response_result': resp.json()})
                    else:
                        rec.write({
                            'json_data': specialization_sync,
                            'status': 0,
                            'response_result': resp.json()})
                        self.env['kw_kwantify_integration_log'].sudo().create(
                            {'name': 'Specialization Master Skill Sync Data',
                             'new_record_log': specialization_sync,
                             'request_params': specializationurl,
                             'response_result': resp.json()})
                        template_id.with_context(mail_id=last_mail_id, model_id=rec.model_id, record_id=rec.rec_id,
                                                 response_result=resp.json()).send_mail(rec.id)
                        self.env.user.notify_success(message='Mail sent successfully')

                else:
                    rec.write({
                        'json_data': specialization_sync,
                        'status': 0,
                        'response_result': resp.json()})
                    self.env['kw_kwantify_integration_log'].sudo().create(
                        {'name': 'Specialization Master Skill Sync Data',
                         'new_record_log': specialization_sync,
                         'request_params': specializationurl,
                         'response_result': resp.json()})
                    template_id.with_context(mail_id=last_mail_id, model_id=rec.model_id, record_id=rec.rec_id,
                                             response_result=resp.json()).send_mail(rec.id)
                    self.env.user.notify_success(message='Mail sent successfully')
            else:
                if resp.status_code == 200:
                    if json_record['status'] == 1:
                        rec.write({
                            'json_data': specialization_sync,
                            'status': 1,
                            'response_result': resp.json()})
                        self.env['kw_kwantify_integration_log'].sudo().create(
                            {'name': 'Specialization Master Sync Data',
                             'new_record_log': specialization_sync,
                             'request_params': specializationurl,
                             'response_result': resp.json()})
                    else:
                        rec.write({
                            'json_data': specialization_sync,
                            'status': 0,
                            'response_result': resp.json()})
                        self.env['kw_kwantify_integration_log'].sudo().create(
                            {'name': 'Specialization Master Sync Data',
                             'new_record_log': specialization_sync,
                             'request_params': specializationurl,
                             'response_result': resp.json()})
                        template_id.with_context(mail_id=last_mail_id, model_id=rec.model_id, record_id=rec.rec_id,
                                                 response_result=resp.json()).send_mail(rec.id)
                        self.env.user.notify_success(message='Mail sent successfully')
                else:
                    rec.write({
                        'json_data': specialization_sync,
                        'status': 0,
                        'response_result': resp.json()})
                    self.env['kw_kwantify_integration_log'].sudo().create({'name': 'Specialization Master Sync Data',
                                                                           'new_record_log': specialization_sync,
                                                                           'request_params': specializationurl,
                                                                           'response_result': resp.json()})
                    template_id.with_context(mail_id=last_mail_id, model_id=rec.model_id, record_id=rec.rec_id,
                                             response_result=resp.json()).send_mail(rec.id)
                    self.env.user.notify_success(message='Mail sent successfully')

    @api.model
    def check_specialization_group(self):
        u_id = self.env['res.users'].sudo().search([('id', '=', self.env.uid)])
        if u_id.has_group('hr.group_hr_manager'):
            return '1'

    # Create method for Specialization master
    @api.model
    def create(self, vals):
        specialization_record = super(kwmaster_specializations, self).create(vals)
        sync_data = self.env['kw_emp_sync_log'].create(
            {'model_id': 'kwmaster_specializations', 'rec_id': specialization_record.id, 'code': False, 'status': 0})
        return specialization_record

    # write method for Specialization master
    @api.multi
    def write(self, vals):
        specialization_record = super(kwmaster_specializations, self).write(vals)
        w_id = self.env['kwmaster_specializations'].sudo().search([('id', '=', self.id)])
        if w_id.write_uid.id != 1:
            log_rec = self.env['kw_emp_sync_log'].sudo().search(
                ['&', '&', ('model_id', '=', 'kwmaster_specializations'),
                 ('rec_id', '=', w_id.id), ('status', '=', 0)])
            if len(log_rec) == 0:
                sync_data = self.env['kw_emp_sync_log'].create(
                    {'model_id': 'kwmaster_specializations', 'rec_id': w_id.id, 'code': False, 'status': 0})
        return specialization_record