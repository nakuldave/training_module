# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 OpenERP SA (<http://www.serpentcs.com>)
#    Copyright (c) Cetco  2014-15 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name':"School Management System",
    'author':"Serpent Consulting Services Pvt. Ltd.",
    'website':"www.serentcs.com",
    'version':"1.0",
    'category':"School",
    'depends':['base', 'sale', "report_webkit"],
    'description':""" 
        This module will provide the student registration features,
        Leave management,
    """,
    'update_xml': ['student_view.xml', 'exam_view.xml',
                   'sequence.xml', 'result_view.xml',
                   'sale_view.xml', 'res_partner_view.xml',
                   'wizard/student_result_summary_view.xml',
                   'wizard/student_range_view.xml',
                   'leave_view.xml',
                   'leave_workflow.xml',
                   'report_view.xml',
                   'data/demo_data.xml',
                   ],
    'data':['data/stream.stream.csv', 'data/year.year.csv'],
    'auto_install':False,
    'application':True,
}
