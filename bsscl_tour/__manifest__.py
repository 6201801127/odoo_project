{
    'name': "My Tour",
    'summary': """My Tour module""",
    'description': "Tour management module",
    'version': '14.0',
    'category' : "Web Application",
    'website': "https://www.bsscl.bihar.co.in",
    'author': 'Ajay',
    'depends' : ['base','hr'],
    'data':['security/ir.model.access.csv',
            'security/tour_security.xml',
            'data/tour_mail_template.xml',
            'wizard/tour_rejection.xml',
            'views/bsscl_expense_type.xml',
            'views/bsscl_guest_house.xml',
            'views/bsscl_medical_expense.xml',
            'views/bsscl_telephone_bill_expense.xml',
            'views/bsscl_tour_advance.xml',
            'views/bsscl_tour_allowance_conf.xml',
            'views/bsscl_tour_classification_expense.xml',
            'views/bsscl_tour_da.xml',
            'views/bsscl_tour_details.xml',
            'views/bsscl_tour_ravel_expense_details.xml',
            'views/bsscl_tour_settlement.xml',
            'views/bsscl_tour.xml',
            'views/tour_city.xml',
            'views/tour_travel_booking.xml',
            'views/menu.xml',],
    'application': True,
    'installable': True,
    'auto_install': False,
    'sequence': 1,
}