# -*- encoding: utf-8 -*-
{
    "name": "BSAP Website",
    "summary": "BSAP Website",
    "description": "BSAP Website",
    "category": "BSAP",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": ["web", "mail", "website", "bsap_cms", "bsap_attendance"],
    "data": [
        "data/bsap_website_menus.xml",
        "security/ir.model.access.csv",
        
        "views/bsap_header.xml",
        "views/homepage.xml",
        "views/bsap_footer.xml",
        "views/bsap_about.xml",
        "views/bsap_faq_page.xml",
        "views/bsap_feedback_page.xml",
        "views/bsap_disclaimer_page.xml",
        "views/bsap_terms_and_condition_page.xml",
        "views/bsap_privacy_policy_page.xml",
        "views/bsap_sitemap_page.xml",
        "views/bsap_help_page.xml",
        "views/bsap_organization _locator_page.xml",
        "views/bsap_emp_notification.xml",
        "views/bsap_rti_page.xml",
        "views/bsap_grievance.xml",
        "views/bsap_manual_page.xml",
        "views/bsap_audit_report_page.xml",
        # "views/bsap_notification.xml",
        "views/bsap_contact_us.xml",
        # "views/bsap_gallery.xml",
        "views/bsap_download_page.xml",
        "views/bsap_login.xml",
        "views/bsap_forget_password.xml",
        "views/bsap_organisation_chart.xml",
        "views/bsap_asset_declaration_page.xml",
        "views/bsap_training_mannual.xml",
        "views/bsap_login.xml",
        # "views/location.xml",
        # "views/bsap_rti_view.xml",
        "views/assets.xml",
    ],
    # 'qweb': [
    #     'static/src/xml/*.xml',
    # ],
}
