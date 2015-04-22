
from osv import osv, fields

class student_result_summary(osv.osv_memory):
    
    _name = 'student.result.summary'
    
    _columns = {
        'subject_id':fields.many2one("subject.subject", "Subject"),
        'mark':fields.float("Mark-1"),
        'mark_2':fields.float("Mark-2")
    }

    _defaults = {
        'mark':60.0,
        'mark_2':70.0,
    }
    
    def get_student_results(self, cr, uid, ids, context=None):
        
        for result_rec in self.browse(cr, uid, ids, context=context):
            
            result_ids = []
            view_ids = self.pool.get('ir.ui.view').search(cr, uid, [('name', '=', 'student.result.tree.view')], context=context)
            if view_ids:
                if result_rec.subject_id:
                    result_line_obj = self.pool.get('result.subject.line')
                    sub_line_ids = result_line_obj.search(cr, uid, [('subject_id', '=', result_rec.subject_id.id),
                                                     ('obtain_marks', '>=', result_rec.mark),
                                                     ('obtain_marks', '<=', result_rec.mark_2)], context=context)
                    if sub_line_ids:
                        for res_line in result_line_obj.browse(cr, uid, sub_line_ids, context=context):
                            result_ids.append(res_line.result_id.id)
                        return {
                           'name' :'Student Result Summary',
                           'res_model': 'student.result',
                           'view_type': 'form',
                           "view_mode": 'form',
                           'type': 'ir.actions.act_window',
                           'views': [(view_ids[0], 'form')],
                           'domain':[('id', 'in', result_ids)],
                        }

        return {'type':'ir.actions.act_window_close'}
