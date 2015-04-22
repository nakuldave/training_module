from osv import osv, fields
from datetime import datetime, timedelta
from tools import DEFAULT_SERVER_DATE_FORMAT

class leave_leave(osv.osv):
     
    _name = 'leave.leave'
     
    _columns = {
        'name':fields.char("Leave Reason", size=64),
        'sdate':fields.date("Start Date"),
        'edate':fields.date("End Date"),
        'strm_id':fields.many2one('stream.stream', "Stream"),
        'student_id':fields.many2one("student.student", "Student"),
        'duration_difference':fields.integer("Duration in days"),
        'state':fields.selection([('draft', 'Draft'), ('request', 'Requested'), ('approve', 'Approved'), ('cancel', 'Cancelled')], string="Status"),
    }
    
    _defaults = {
        'state':'draft',
    }
    
    def set_to_request(self, cr, uid, ids, context=None):
        
        print "Hey, I am cold...."
        self.write(cr, uid, ids, {'state':'request'}, context=context)
        return True
    
    def check_duration(self, cr, uid, ids, start_date, end_date, context=None):
       
        if start_date and end_date:
            st_date = datetime.strptime(start_date, DEFAULT_SERVER_DATE_FORMAT)
            en_date = datetime.strptime(end_date, DEFAULT_SERVER_DATE_FORMAT)
            if st_date > en_date:
                raise osv.except_osv(_('Amri error'), _("Start Date cannot be greater than end date!"))
            difference = st_date - en_date
            return {'value':{'duration_difference':abs(difference.days)}}
        
        return {}
