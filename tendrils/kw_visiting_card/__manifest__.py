{
    "name": "Kwantify Business Card Requisition",
    "summary": " Business Card for employees of the organization",
    'description': " Business Card for employees of the organization",
    "website": "https://www.csm.tech",
    "author": "CSM Technologies",
    'application': True,
    'installable': True,
    'auto_install': False,
    "depends": [
        'base', 'hr', 'mail', 'kw_dynamic_workflow', 'kw_employee',
    ],
    "data": [
        'security/apply_card_security.xml',
        'security/ir.model.access.csv',
        'views/menuitem.xml',
        'views/apply_card.xml',
        # 'views/archieved_application.xml',
        'views/card_details_view.xml',
        'views/email/apply_visiting_card_mail_template.xml',
        'views/email/status_apply_mail_template.xml',
        'data/kw_visiting_card_dynamic_workflow.xml',
        # 'data/kw_visiting_card_activity.xml',
        'views/apply_card_report_view.xml',
        'views/apply_card_take_action_view.xml',
        
        # 'views/assets.xml',
        'views/res_partner_form_view.xml',
        'data/kw_visiting_card_expire_cron.xml',
        'views/email/ra_approve_manager_mail_template.xml',
        'views/email/ra_auto_escalated_mail_template.xml',
        'views/email/send_for_print_template.xml',
        'wizard/send_printing_email_wizard_view.xml',
    ],
}