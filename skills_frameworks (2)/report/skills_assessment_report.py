import time
from openerp.osv import osv
from openerp.report import report_sxw
from datetime import datetime


class skill_assessment_report(report_sxw.rml_parse):


    def __init__(self, cr, uid, name, context=None):
        super(skill_assessment_report, self).__init__(cr, uid, name, context=context)
        self.index = 0
        self.index1 = 0
        self.localcontext.update({
            
            'time': time,
            'get_index' : self.get_index,
            'get_index1' : self.get_index1,
            
            })
            
    def get_index(self):
        self.index += 1
        return self.index

    def get_index1(self):
        self.index1 += 1
        return self.index1
    

class skill_assessment_report_template_id(osv.AbstractModel):
    _name = 'report.skills_frameworks.skill_assessment_report_template_id'
    _inherit = 'report.abstract_report'
    _template = 'skills_frameworks.skill_assessment_report_template_id'
    _wrapped_report_class = skill_assessment_report

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
