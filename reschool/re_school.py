from openerp.osv import fields,osv
from datetime import date, time
from tools.translate import _ 



class student_student(osv.Model):
    
    _name = "student.student"
    
    _columns = {
        'name':fields.char("Student Name"),
        'dob':fields.date("Date_of_birth"),
        'age':fields.integer("Student Age"),
        'standard':fields.integer("Student Grade"),        
        }
    
    
#class school_school(osv.Model):
#    
#    _name = "school.school"
#    
#    _columns = {
#        'name':
#                
#                }