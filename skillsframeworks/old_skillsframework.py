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
    }
    
class skillsframework_category (osv.Model):
    _name = "skillsframework.category"
    _description = "Framework Categories"
    
    _columns = {
        'name': fields.char('Name', size=64,required=True),
        'framework_id': fields.many2one('skillsframework.framework','Framework',required=True),
        'parent_id': fields.many2one('skillsframework.category','Parent Category',ondelete='cascade' ),
        'child_id': fields.many2one('skillsframework.category','Child Category'),
        'priority': fields.integer('Display Order'),
        'description': fields.text('Description'), 
        'colour':fields.char('Hex Colour', size=7),
    }
    _defaults = {
           'priority': 5,
       }

    
class skillsframework_skill (osv.Model):
    _name = "skillsframework.skill"
    _description = "Category Skills"

    _columns = {
        'name': fields.char('Name', size=64,required=True),
        'code':fields.char('Code'),
        'description': fields.text('Description'),
        'category_id': fields.many2one('skillsframework.category','Category',ondelete='cascade',required=True),
        'priority': fields.integer('Display Order'),
    }
    _defaults = {
           'priority': 5,
       }
class skillsframework_competency (osv.Model):
    _name = "skillsframework.competency"
    _description = "Skills Competency"

    _columns = {
        'level': fields.integer('Competency Level'),
        'description': fields.text('Description'),
        'skill_id': fields.many2one('skillsframework.skill','Skill',ondelete='cascade',required=True),
        'skillcode':fields.related('skill_id', 'code', type='char', string='Skill Code'),
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
         
    }
    _defaults = {
           'is_selfassessed': True,
       }
class hr_employee(osv.Model):
    _inherit = "hr.employee"
    _columns = {
        'employeeskills_ids' : fields.one2many('skillsframework.employeeskills', 'employee_id', 'Employee Competencies'),
    }
