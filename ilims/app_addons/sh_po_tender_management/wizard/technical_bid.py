from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from datetime import date, datetime


class OpenTechnicalWizard(models.TransientModel):
    _name = 'open.technical.wizard'

    technical_bid_ids = fields.One2many('open.technical.wizard.lines', 'open_technical_id')

    @api.model
    def default_get(self, fields):
        rec = super(OpenTechnicalWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            tender = self.env['purchase.agreement'].search([('id', '=', active_id)], limit=1)
            rfqs = self.env['purchase.order'].search([('agreement_id', '=', tender.id), ('state', '=', 'draft')])
            if tender.technical_bid_opening_date > datetime.now():
                raise ValidationError(_("Tender is still in Bid Processing!"))
            if not rfqs:
                raise ValidationError(_("No Quotation been generated by Vendor yet!"))
            rfq_list = []
            if rfqs:
                for rfq in rfqs:
                    rfq_list.append([0, 0, {
                        'open_technical_id': self.id,
                        'po_number': rfq.id,
                        'vendor_id': rfq.partner_id.id,
                        'technical_document': rfq.sh_technical_attachment,
                        'technical_document_name': rfq.sh_technical_attachment_name
                    }])
            rec['technical_bid_ids'] = rfq_list
            user_list = ''
            if tender.project_id and tender.project_id.user_id.partner_id.email:
                user_list += tender.project_id.user_id.partner_id.email + ", "
            elif tender.project_id and tender.project_id.user_id:
                user_list += tender.project_id.user_id.login + ", "
            if tender.project_id and tender.project_id.program_manager_id.partner_id.email:
                user_list += tender.project_id.program_manager_id.partner_id.email + ", "
            elif tender.project_id and tender.project_id.program_manager_id:
                user_list += tender.project_id.program_manager_id.login + ", "
            if tender.partner_ids:
                for partner in tender.partner_ids:
                    if partner.email:
                        user_list += partner.email
            template = self.env.ref('sh_po_tender_management.tender_email_on_technical_marks_publish')
            if template:
                values = template.generate_email(tender.id, ['subject', 'email_to', 'email_from', 'body_html'])
                values['email_to'] = user_list
                values['email_from'] = self.env.user.partner_id.email or self.env.user.login
                values['body_html'] = values['body_html']
                mail = self.env['mail.mail'].create(values)
                try:
                    mail.send()
                except Exception:
                    pass
        return rec

    def publish_technical(self):
        if any(lines.technical_marks is 0 for lines in self.technical_bid_ids):
            raise UserError(_("Please fill the Technical Marks for all Vendor!"))
        active_id = self.env.context.get('active_id')
        if active_id:
            tender = self.env['purchase.agreement'].search([('id', '=', active_id)])
            for lines in self.technical_bid_ids:
                if lines.po_number:
                    lines.po_number.update({'technical_marks': lines.technical_marks})
            if tender:
                tender.write({'state': 'technical_bid'})


class OpenTechnicalWizardLines(models.TransientModel):
    _name = 'open.technical.wizard.lines'

    open_technical_id = fields.Many2one('open.technical.wizard')
    po_number = fields.Many2one('purchase.order', 'RFQ')
    vendor_id = fields.Many2one('res.partner', 'Vendor')
    technical_document = fields.Binary('Download Technical Document')
    technical_document_name = fields.Char('Download Technical Document Filename')
    technical_marks = fields.Integer('Technical Marks')
