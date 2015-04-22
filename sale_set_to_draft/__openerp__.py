# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################

{
    'name':' Sale Set To Draft',
    'version':'1.0',
    'description': """
         This Module is used to set quotation to draft state after when you confirm sale order 
         and cancel quotation in odoo

    """,
    'author':'BrowseInfo',
    'website':'http://www.browseinfo.in',
    'images':[],
    'data': [
            'sale_set_to_draft.xml',
            ],
    'depends':['sale'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

