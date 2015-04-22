from osv import osv, fields
from datetime import datetime
from tools import DEFAULT_SERVER_DATE_FORMAT
from tools.translate import _

class exam_exam(osv.osv):
    
    _name = 'exam.exam'
    
    def _get_duration(self, cr, uid, ids, name, args, context=None):
        
        print "browse Records in list LL", self.browse(cr, uid, ids, context=context)
        res = {}
        for exam_rec in self.browse(cr, uid, ids, context=context):
            if exam_rec.start_date and exam_rec.end_date:
                s_date = datetime.strptime(exam_rec.start_date, DEFAULT_SERVER_DATE_FORMAT)
                e_date = datetime.strptime(exam_rec.end_date, DEFAULT_SERVER_DATE_FORMAT)
                difference = e_date - s_date
                diff_days = difference.days
                res[exam_rec.id] = diff_days
            else:
                res[exam_rec.id] = 0 
        return res
    
    _columns = {
        'name':fields.char("Description", size=64),
        'exam_code':fields.char("Exam Code", size=64),
        'start_date':fields.date("Start Date"),
        'end_date':fields.date("End Date"),
        'stream_id':fields.many2one("stream.stream", "Stream"),
        "student_ids":fields.many2many("student.student",
                                       "exam_student_rel",
                                       "exam_id",
                                       "student_id", "Student"),
                
        "exam_duration":fields.function(_get_duration, type="integer", string="Exam Duration"),
    }
    
    def check_date(self, cr, uid, ids, start_date, end_date, context=None):

        """
        @self : Current Class Pointer
        @cr : Database Cursor
        @uid : Logged in User ID
        @ids : List of Ids
        @start_date : Start Date value passed from xml file
        @end_date : End Date value passed from xml file
        @context : Standard Dictionary
        @return : check the date and if wrong value entered will 
                    raise the warning
        """
        res = {}
        if start_date and end_date:
            s_date = datetime.strptime(start_date, DEFAULT_SERVER_DATE_FORMAT)
            e_date = datetime.strptime(end_date, DEFAULT_SERVER_DATE_FORMAT)
            if s_date > e_date:
                # Value Dictiionary
                res.update({'start_date':False, 'end_date':False}) 
                
                # Warnning Dictionary
                warning = {
                           'title': _('User Error !'),
                           'message': _('Start Date Cannot be greater than enddate!')
                }
                return {'value':res, 'warning':warning}
    #             raise osv.except_osv(_('User Error!'),
    #                                  _('Start Date Cannot be greater than enddate!'))
        return res
