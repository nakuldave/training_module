from openerp.osv import fields, osv
from openerp import tools

class skillsframework_jobrole (osv.Model):
    _name = "skillsframework.jobrole"
    _description = "Job Roles"
    _columns = {
        'name': fields.char('Name', size=64),
        'description': fields.text('Description'),
    }

class skillsframework_jobcompetency (osv.Model):
    _name = "skillsframework.jobcompetency"
    _description = "Job Competencies"
    _columns = {
         'jobrole_id': fields.many2one('skillsframework.jobrole', 'Job Role',required=True),
         'competency_id': fields.many2one('skillsframework.competency', 'Competency',required=True),
              
        'skillcode':fields.related('competency_id', 'skillcode', type='char', string='Skill Code'),
        'skilllevel':fields.related('competency_id', 'level', type='integer', string='Competency Level'),
         
         'description' : fields.text('Description'),
         
    }
    
    
class skillsframework_framework (osv.Model):
    _name = "skillsframework.framework"
    _description = "Base Framework"

    
    
    _columns = {
        'name': fields.char('Name', size=64),
        'description': fields.text('Description'),
        'is_active': fields.boolean('Is Active',help="Specify if the Framework is Active"),
        'category_id' : fields.one2many('skillsframework.category', 'framework_id','Categories'),
        'skill_id' : fields.one2many('skillsframework.skill', 'framework_id', 'Skills'),
        'competency_id' : fields.one2many('skillsframework.competency', 'framework_id', 'Competencies'),

        
    }
    
class skillsframework_category (osv.Model):
    _name = "skillsframework.category"
    _description = "Framework Categories"
    
    
    def _get_child_ids(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for record in self.browse(cr, uid, ids, context=context):
            if record.child_parent_ids:
                result[record.id] = [x.id for x in record.child_parent_ids]
            else:
                result[record.id] = []
                
            if record.child_consol_ids:
                for ski in record.child_consol_ids:
                    if ski.id not in result[record.id]:
                        result[record.id].append(ski.id)

        return result
        
    
    
    
    _columns = {
        'name': fields.char('Name', size=64,required=True),
        'framework_id': fields.many2one('skillsframework.framework','Framework',required=True),
        'parent_category_id': fields.many2one('skillsframework.category','Parent Category',ondelete='cascade' ),
        'child_category_id': fields.function(_get_child_ids, type='many2many', relation="skillsframework.category", string="Child Category"),
        'child_parent_ids': fields.one2many('skillsframework.category','parent_category_id','Children'),
        'child_consol_ids': fields.many2many('skillsframework.category', 'skill_skill_consol_rel', 'child_id', 'parent_id', 'Consolidated Children'),
        'priority': fields.integer('Display Order'),
        'description': fields.text('Description'), 
        'colour':fields.char('Hex Colour', size=7),
        'skill' : fields.one2many('skillsframework.skill', 'category_id', 'Skills'),
        'skill_competency' : fields.one2many('skillsframework.competency', 'skill_categ', 'Competencies'),
        
    }
    _defaults = {
           'priority': 5,
       }
       
    _order = "priority"

    
class skillsframework_skill (osv.Model):
    _name = "skillsframework.skill"
    _description = "Category Skills"

    _columns = {
        'name': fields.char('Name', size=64,required=True),
        'code':fields.char('Code'),
        'description': fields.text('Description'),
        'category_id': fields.many2one('skillsframework.category','Category',ondelete='cascade',required=True),
        'priority': fields.integer('Display Order'),
        'framework_id': fields.many2one('skillsframework.framework', 'Framework'),
    }
    _defaults = {
           'priority': 5,
       }
       
    _order = "priority"
class skillsframework_competency (osv.Model):
    _name = "skillsframework.competency"
    _description = "Skills Competency"

    def _name_conct(self, cr, uid, ids, field_name, arg, context=None):
        print 'ids-----',ids
        res={}
        if ids:
            for id in ids:
                br_recs=self.browse(cr, uid, id)
                print 'br_recs------',br_recs
                str1=str(br_recs.skillcode) + '-' + str(br_recs.level)
                res[id] = str1
        return res
            

    _columns = {
        'level': fields.integer('Competency Level'),
        'description': fields.text('Description'),
        'skill_id': fields.many2one('skillsframework.skill','Skill',ondelete='cascade',required=True),
        'skillcode':fields.related('skill_id', 'code', type='char', string='Skill Code'),
        'name' : fields.function(_name_conct, type='char', string='Name'),
        'skill_categ' : fields.many2one('skillsframework.category', 'Skill Category'),
        'framework_id': fields.many2one('skillsframework.framework', 'Framework'),
    }
    
    
class skillsframework_employee_skills (osv.Model):
    _name = "skillsframework.employeeskills"
    _description = "Employee Competencies"
    _columns = {
         'employee_id': fields.many2one('hr.employee', 'Employee',required=True),
         'competency_id': fields.many2one('skillsframework.competency', 'Competency',required=True),
              
        'skillcode':fields.related('competency_id', 'skillcode', type='char', string='Skill Code'),
        'skilllevel':fields.related('competency_id', 'level', type='integer', string='Competency Level'),
         
         'is_selfassessed':   fields.boolean('Is Self Assessed',help=""),
         'date_awarded': fields.date('Date Awarded'),
         'date_expires': fields.date('Date Expires'),
         'evidence' : fields.text('Supporting Evidence'),
         'framework_name' : fields.many2one('skillsframework.framework', 'Framework Name'),
         
    }
    
#    _rec_name = "framework_name"
    
    _defaults = {
           'is_selfassessed': True,
       }
       
#class skillsframework_manage_framework (osv.Model): 
#   _name = "skillsframework.manage.framework"
#   _description = "Framework Management"
#   _columns = {
#       'parent_id': fields.many2one('skillsframework.manage.framework', 'Parent', ondelete='cascade'),
    
    
#   }
       
       
class hr_employee(osv.Model):
    _inherit = "hr.employee"
    _columns = {
        'self_assessed_skills' : fields.many2many('skillsframework.employeeskills', 'self_ass_skill', 'self_id', 'hr_self_rel', 'Self'),
        'formally_assessed_skills' : fields.many2many('skillsframework.employeeskills', 'form_ass_skill', 'asse_id', 'hr_formal_rel', 'Formal'),
    }
    
