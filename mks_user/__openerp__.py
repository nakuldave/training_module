# -*- encoding: utf-8 -*-
{

    'name' : 'MKS USER Wizard',  
    'version' : '1.0',
    'author' : 'MKS',
    'category' : 'General',
    'depends' : ['base'],
    'description' : """
                        MKS USER Management Wizard

""",
    
    "init_xml" : [],
    "demo_xml" : [],


    "update_xml" : [
                    'security/user_form_security.xml',
                    "wizard/user_create_wizard_view.xml",
                     ],

    "active": False 
}
