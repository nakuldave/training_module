
from osv import osv, fields

class student_range(osv.osv_memory):
    
    _name = 'student.range.summary'
    
    _columns = {
        'date_from':fields.date("Date From", required=True),
        'date_to':fields.date("Date To", required=True),
    }

    def get_print(self, cr, uid, ids, context=None):
        
        student_obj = self.pool.get('student.student')
        self.read(cr, uid, ids[0], context=context)
        for wiz_data in self.browse(cr, uid, ids, context=context):
            
            print "Date from ", wiz_data.date_from
            print "Date To :::", wiz_data.date_to
            student_ids = student_obj.search(cr, uid, [('registration_date', '>=', wiz_data.date_from),
                                                       ('registration_date', '<=', wiz_data.date_to)])
            print "Students IDs:::::::;", student_ids
#             res = self.read(cr, uid, ids, context=context)
            res = {
                'ids':student_ids,
                'model':'student.student',
                'context':context,
             }
            return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'student.info.rep',
                    'datas': res,
                }
            
        return {'type':'ir.actions.act_window_close'}
