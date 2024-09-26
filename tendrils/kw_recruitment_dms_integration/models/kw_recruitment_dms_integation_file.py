# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.addons.kw_dms_utils.tools import file


class DmsRecruitmentIntegration(models.AbstractModel):
    _name = 'kw_dms.kw_recruitment.integration'
    _description = 'DMS File Integration Mixin For Recruitment'

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    content_file = fields.Binary(compute='_compute_content', inverse='_inverse_content',
                                 string='Content', attachment=False, readonly=False, prefetch=False, store=False)

    file_name = fields.Char(string="Filename", compute='_compute_content',
                            # inverse='_inverse_content',
                            readonly=False, store=True, )

    dms_file_id = fields.Many2one(string='DMS File ID', comodel_name='kw_dms.file', ondelete='restrict', )

    def _compute_content(self):
        for record in self:
            if record.dms_file_id and record.dms_file_id.permission_read:
                record.content_file = record.dms_file_id.content or False
                record.file_name = record.dms_file_id.name or False

    @api.multi
    def _inverse_content(self):
        for record in self:
            if record.dms_file_id:
                record.dms_file_id.write({'content': record.content_file})

    @api.model
    def create(self, vals_list):
        new_rec = super(DmsRecruitmentIntegration, self).create(vals_list)
        if vals_list.get('res_model') == 'hr.applicant':
            if 'content_file' in vals_list:
                new_rec.create_dms_file(vals_list['content_file'], vals_list['file_name'])
        return new_rec

    @api.multi
    def write(self, vals_list):
        update_rec = super(DmsRecruitmentIntegration, self).write(vals_list)
        if vals_list.get('res_model') == 'hr.applicant':
            if 'content_file' in vals_list:
                self.create_dms_file(vals_list['content_file'], vals_list['file_name'])
        return update_rec

    def create_dms_file(self, content_file, file_name):
        """##create file record"""
        model_rec = self.env['ir.model'].sudo().search([('model', '=', self._name)])
        if model_rec and content_file:
            applicant_id = self.env['hr.applicant'].sudo().browse(self.applicant_id.id)
            directory = applicant_id.dms_user_doc_dir_id
            if directory:
                name = self.name_get()[0][1]
                # extension = file.guess_extension(file_name)
                # if directory.root_storage.activate_versioning:
                #     file_name = "%s_%s.%s" % (
                #         file.slugify(file_name), str(1.0), extension)
                # else:
                #     file_name = "%s.%s" % (file.slugify(file_name), extension)
                dms_file_rec = self.env['kw_dms.file'].create({
                    'name': file_name,
                    'document_name': file_name,
                    'version': 1.0,
                    'content': content_file,
                    'directory': directory.id,
                    'res_id': self.applicant_id.id,
                    'res_name': name,
                    'res_model': model_rec.model,
                    'res_model_name': model_rec.name
                })
                self.dms_file_id = dms_file_rec.id
            else:
                applicant_id._create_recruitment_cv_folder()
                if applicant_id.create_date:
                    self.create_dms_file(content_file, file_name)

    def create_dms_file_with_resid(self, content_file, file_name, res_id):
        """# method for the scheduler"""
        model_rec = self.env['ir.model'].sudo().search([('model', '=', 'ir.attachment')])
        if model_rec and content_file:
            # attachment_id = self.env['ir.attachment'].sudo().browse(res_id)
            applicant_id = self.env['hr.applicant'].sudo().browse(res_id.res_id)
            directory = applicant_id.dms_user_doc_dir_id
            # print(directory)

            if directory:
                name = directory.name_get()[0][1]
                extension = file.guess_extension(file_name)

                if directory.root_storage.activate_versioning:
                    file_name = "%s_%s.%s" % (file.slugify(name), str(1.0), extension)
                else:
                    file_name = "%s.%s" % (file.slugify(name), extension)

                dms_file_rec = self.env['kw_dms.file'].create({
                    'name': res_id.datas_fname,
                    'document_name': name,
                    'version': 1.0,
                    'content': content_file,
                    'directory': directory.id,
                    'res_id': res_id.id,
                    'res_name': name,
                    'res_model': model_rec.model,
                    'res_model_name': model_rec.name
                })
                res_id.write({'dms_file_id': dms_file_rec.id})
            else:
                applicant_id._create_recruitment_cv_folder()
                if applicant_id.create_date:
                    self.create_dms_file_with_resid(content_file, file_name, res_id)
