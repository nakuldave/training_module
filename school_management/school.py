from openerp.osv import fields,osv
from datetime import datetime,date
from tools.translate import _

class school_school (osv.Model):
    
    _name = 'school.school'
    
    def create(self, cr, uid, vals, context=None):
        res={}
        if not vals.get('code'):
            vals.update({'code':vals.get('name')})
        return super(school_school, self).create(cr, uid, vals, context=context)
    
    def write(self,cr,uid,ids,vals,context=None):
        if vals.get('code'):
            raise osv.except_osv(_('Error!'),_('You Cannot Change the Code'))
        return super (school_school, self).write(cr,uid,ids,vals,context=context)
    
    _columns ={
                'name': fields.char('School Name'),
                'established': fields.date('Established Date'),
                'code': fields.char('Code'),
                'contact': fields.char('Contact Number'),
                'student_ids': fields.one2many('student.student','school_id','StudentID'),
               }
    
class student_student (osv.Model):
    _name = 'student.student'

    status_selection = [('draft', 'New'),
                        ('process', 'In Progress'),
                        ('approve', 'Done'),
                        ('cancel', 'Rejected')]

    def _full_name(self, cr, uid, ids, fields, arg, context=None):

        res={}
        for record in self.browse(cr, uid, ids,context=context):
            if not record.lname:
                res[record.id]=record.name
                return res
            else:
                res[record.id]=record.name+' '+record.lname
        return res

    def get_address(self, cr, uid, ids, customer_id, context=None):

        res = {}
        if customer_id:
            partner_rec = self.pool.get('res.partner').browse(cr, uid, customer_id, context=context)
            res = {'value':{'street':partner_rec.street or "",
                            'street2':partner_rec.street2 or "",
                            'city':partner_rec.city or "",
                            'state_id':partner_rec.state_id and partner_rec.state_id.id or False,
                            'zip':partner_rec.zip or "",
                            'country_id':partner_rec.country_id and partner_rec.country_id.id or False,
                            }}
        return res

    def get_admissiondate(self,cr,uid,ids,dob,context=None):
        res = {}
        d=datetime.strptime(dob,'%Y-%m-%d')
        y=d.year+5
        m=d.month
        d=d.day
        
        m=str(m)
        d=str(d)
        y=str(y)
        fin=m+'/'+d+'/'+y
        print ":::::::",type(fin)
        res={'value':{'admission_date':fin}}
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

    def set_to_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':"draft"}, context=context)
        return True 

    _columns={
              'partner_id':fields.many2one('res.partner', "Partner"),
              'name':fields.char('Student Name'),
              'lname':fields.char('Last Name'),
              'dob':fields.date('Date of Birth'),
              'admission_date':fields.char('Admission Date'),
              'contact':fields.char('Contact Number'),
              'school_id':fields.many2one('school.school','School'),
              'full_name':fields.function(_full_name,type='char',string='Full Name'),
              'street':fields.char('street'),
              'customer_id':fields.many2one('res.partner', "customer"),
              'street2':fields.char('street2'),
              'city':fields.char('city'),
              'state_id':fields.many2one('res.country.state',"State"),
              'zip':fields.char('Zip'),
              'country_id':fields.many2one('res.country', "Country"),
              'state':fields.selection(status_selection, "State"),
              'student_ids':fields.one2many('result.result','result_id','Student')
              }
    
    _sql_constraints =  [
                        ('student_name_unique',
                         'unique(name)',
                         'Name Already Exists Please Enter a New Name'),
                        ]
    
    def check_date(self, cr, uid, ids, context=None):

        res = {}
        current_date = date.today()
        for rec in self.browse(cr, uid, ids, context=context):
            if rec.dob and rec.dob > str(current_date):
                return False
        return True

    _constraints = [(check_date, 'Enter Value is not correct!', ['dob'])]

    
    _defaults = {
        'state':'draft'
                }

class result_result (osv.Model):

    _name = 'result.result'
    
    def _final_result(self, cr, uid, ids, fields, arg, context=None):

        res={}
        for record in self.browse(cr, uid, ids,context=context):
            if record.obtained_marks >= record.passing_marks:
                res[record.id]="Pass"
            else:
                res[record.id]="Fail"
        return res
    
#    def get_studentname(self, cr, uid, ids,result_id,context=None):
#        res = {}
#        if result_id:
#            student_rec =  self.pool.get('student.student').browse(cr, uid, result_id, context=context)
#            res = {'value':{'name': student_rec.name or ''}}
#        return res
    
    def get_customername(self, cr, uid, ids,result_id,context=None):
        
        res = {}
        if result_id:
            partner_rec = self.pool.get('student.student').browse(cr, uid, result_id, context=context)
            res = {'value':{'name': partner_rec.name or '',
                            'customer_id': partner_rec.customer_id and partner_rec.customer_id.id or False
                            }}
        return res

    _columns = {
                'name':fields.char('Name'),
                'subject_name':fields.char('Subject Name'),
                'obtained_marks': fields.float('Obtained Marks'),
                'maximum_marks': fields.integer('Maximum Marks'),
                'result_id': fields.many2one('student.student','Student Name'),
                'passing_marks': fields.integer('Passing Marks'),
                'final_result':fields.function(_final_result,type='char',string='Final Result'),
                'student_ids':fields.many2one('result.result','student Result'),
                'customer_id':fields.many2one('res.partner','customer')
                }

    def check_marks(self, cr, uid, student_ids, context=None):

        res = {}
        for rec in self.browse(cr, uid, student_ids, context=context):
            if rec.obtained_marks > rec.maximum_marks:
                return False
        return True

    _constraints = [(check_marks, 'Enter Value is not correct!', ['obtained_marks'])]