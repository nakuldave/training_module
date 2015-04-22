{
    'name':'Skills Frameworks',
    'version': '1.5',
    'description':"""
        Skills Framework: frameworks, categories, skills and competency levels to bind to Employees
    """,
    'author':'Jay 4 Pty Ltd',
    'website': 'http://www.jay4.biz',
    'depends': ['base_setup', 'hr'],
    'data': [
        'view/skills_assessment_report_view.xml',        
        'report/skills_assessment_report_menu.xml',
		'skills_frameworks_view.xml',
        'security/skillsFrameworks.xml',
        'security/ir.model.access.csv',
		],
    'demo': [],
    'installable': True,
    'auto_install': False,
}


