from osv import osv, fields
from datetime import datetime, date
from tools.translate import _

import time
from aptsources.sourceslist import uniq

class student_student(osv.osv):
    
    _name = 'student.student'
    
    status_selection = [('draft', 'New'),
                        ('process', 'In Progress'),
                        ('approve', 'Approved'),
                        ('cancel', 'Rejected')]
    
    _order = 'gender'
    
    def unlink(self, cr, uid, ids, context=None):
        
        """
        To raise the User define message that record cannot be deleted for this table
        """
        raise osv.except_osv(_('User Error'), _('You cannot delete this record'))
        res = super(student_student, self).unlink(cr, uid, ids, context=context)
        
        return res
    
    def copy(self, cr, uid, id, default=None, context=None):
        """
        When record will be duplicated we set name and last name as blank.
        """
        default.update({'name':"", 'lname':""})
        res = super(student_student, self).copy(cr, uid, id, default=default, context=context)
        return res
        
    _inherits = {
                 'res.partner':'partner_id'
                 }
    
    _columns = {
                
        'partner_id':fields.many2one('res.partner', "Partner"),
        'sequence':fields.char("Student ID", size=64),
        'image':fields.binary("Image"),
        'lname':fields.char('Last Name', size=64),
        'registration_date':fields.date("Registration Date"),
        'dob':fields.date("Date of Birth"),
        'contact':fields.char("Contact No", size=12),
        'gender':fields.selection([('male', 'Male'), ('female', 'Female')], string="Gender"),
        'comment':fields.text("Note"),
        'stream_id':fields.many2one('stream.stream', "Stream"),
        'year_id':fields.many2one('year.year', "Year"),
        'ref_ids':fields.one2many('reference.reference', 'student_id', string="References"),
        'degree_ids':fields.one2many('degree.degree', 'stud_id', string="Degree"),
        'language_ids':fields.many2many('language.language', 'student_language_rel',
                                        'student_id', 'lang_id', "Languages Known"),
        'hobbies_ids':fields.many2many('hobbies.hobbies',
                                       'student_hobbies_rel', 'student_id',
                                       'hobby_id', "Hobbies"),
        'leader_id':fields.many2one('res.partner', "Leader", required=True),
        'leader_email':fields.char("Leader Email", size=64),
        'is_customer':fields.related('leader_id', 'customer', type="boolean", string="Is Customer?", store=True),
        'state':fields.selection(status_selection, "Status")
    }
    
    _sql_constraints = [
#                         ('check_contact_no',
#                          'CHECK(length(contact)>=10)', "Enter number must be at least 10 digits"),
                        ('student_name_uniqe',
                         'unique(name,lname)',
                         'you cannot enter duplicate name for student'),
                        ]
    
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        
        res = super(student_student, self).search(cr, uid, args, offset, limit=limit, order=order, context=context, count=count)
        
        return res
    
    def check_email_address(self, cr, uid, ids, context=None):
        
        for student in self.browse(cr, uid, ids, context=context):
            if student.leader_email:
                if len(student.leader_email) >= 7 :
                    email_val = student.leader_email
                    if email_val.isalnum():
                        return  True
                    else:
                       return False
                else:
                    return False
            else:
                return False
                
    _constraints = [(check_email_address, 'Enter Value is not correct!', ['leader_email']), ]
    
    def create(self, cr, uid, vals, context=None):
        
        next_sequence = self.pool.get('ir.sequence').get(cr, uid, 'student.student.code')
        vals.update({'sequence':next_sequence})
        res = super(student_student, self).create(cr, uid, vals, context=context)
        
        return res
    
    def set_in_process(self, cr, uid, ids, context=None):
         
        self.write(cr, uid, ids, {'state':"process"}, context=context)
        
        return True
    
    def set_to_approve(self, cr, uid, ids, context=None):
         
        self.write(cr, uid, ids, {'state':"approve"}, context=context)
        
        return True 
    
    def set_to_cancel(self, cr, uid, ids, context=None):
         
        self.write(cr, uid, ids, {'state':"cancel"}, context=context)
        
        return True
    
    def get_leader_email(self, cr, uid, ids, leader_id, context=None):
        
        """
        To get the email from leader and reset to blank if not selected.
        """
        
        # Define objects
        res = {}
#         partner_obj = self.pool.get('res.partner')
        if leader_id:
            partner_rec = self.pool.get('res.partner').browse(cr, uid, leader_id, context=context)
            final_result = {'value':{'leader_email':partner_rec.email or ""}}
            return final_result
        else:
            return {'value':{'leader_email':""}}
    
    def get_date_val(self, cr, uid, context=None):
         
#          current_date = fields.date.context_today
        current_date = date.today()
        final_date = datetime.strftime(current_date, "%d/%m/%Y")
        
        return current_date
     
    def get_next_student_id(self, cr, uid, context=None):
        
        next_sequence = self.pool.get('ir.sequence').get(cr, uid, 'student.student.code')
        
        return next_sequence
    
    _defaults = {
        'gender':'male',
#         'registration_date':lambda *a: time.now().strftime("%Y/%m/%d")
#         'registration_date':fields.date.context_today,
        'registration_date':fields.date.context_today,
        'state':'draft',
#         'sequence': lambda  self, cr, uid , context: self.pool.get('ir.sequence').get(cr, uid, 'student.student.code'),
#         'sequence':get_next_student_id,
    }
    
    def set_student_ID(self, cr, uid, ids, context=None):
        
        student_ID = self.pool.get('ir.sequence').get(cr, uid, 'student.student.code')
        self.write(cr, uid, ids, {'sequence':student_ID, 'state':"approve"}, context=context)
        return True
    
class stream_stream(osv.osv):

    _name = 'stream.stream'
    
    _rec_name = 'code'
    
    _columns = {
        'code':fields.char("Code", size=4),
        'name':fields.char("Name", size=64),
    }
    
class year_year(osv.osv):
    
    _name = 'year.year'
    
    _columns = {
        'name':fields.char("Year", size=8),
        'code':fields.char("Code", size=4),
    }
     
    def name_get(self, cr, uid, ids, context=None):
         
        res = super(year_year, self).name_get(cr, uid, ids, context=context)
         
        final_result = []
        year_ids = []
        if ids:
#             if isinstance(ids, int):
#                 year_ids.append(ids)
#             elif isinstance(ids, list):
#                 year_ids += ids
            for year in self.browse(cr, uid, ids, context=context):
                year_data = ""
                year_data += year.name or ""
                year_data += " ["
                year_data += year.code or ""
                year_data += "]"
                final_result.append((year.id, year_data))
            return final_result
             
        return res

class reference_reference(osv.osv):
    
    _name = 'reference.reference'
    
    _columns = {
        'student_id':fields.many2one('student.student', ondelete='cascade', string="Student"),
        'name':fields.char('Name', size=64),
        'contact':fields.char("Contact No", size=12),
        'email':fields.char("Email", size=64),
    }

class degree_degree(osv.osv):
    
    _name = 'degree.degree'
    
    _description = "Degree Detail"
    
    _columns = {
        'stud_id':fields.many2one('student.student', ondelete='cascade', string="Student"),
        'name':fields.char('Univery Name', size=64),
        'year_id':fields.many2one('year.year', "Year"),
        'stream_id':fields.many2one('stream.stream', "Stream"),
        'percentage':fields.float("Percentage"),
        'status':fields.selection([('pass', 'Pass'), ('fail', 'Fail')], "Status"),
    }
    
    _defaults = {
        'status':'pass',
    }


class language_language(osv.osv):
    
    _name = 'language.language'
    
    _columns = {
        'code':fields.char('Code', size=6),
        'name':fields.char('Name', size=24),
    }

class hobbies_hobbies(osv.osv):
    
    _name = 'hobbies.hobbies'
    
    _columns = {
        'name':fields.char("Name", size=64),
    }
    

