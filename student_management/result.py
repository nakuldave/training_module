from osv import osv, fields

class student_result(osv.osv):
    
    _name = 'student.result'
    
    _columns = {
        'stream_id':fields.many2one('stream.stream', "Stream"),
        'student_id':fields.many2one('student.student', "Student", required=True),
        'year_id':fields.many2one('year.year', "Year"),
        'subjects_line':fields.one2many('result.subject.line', 'result_id', "Subject Details"),
    }

class result_subject_line(osv.osv):
    
    _name = 'result.subject.line'
    
    _columns = {
        'result_id':fields.many2one('student.result', "Result"),
        'subject_id':fields.many2one('subject.subject', "Subject"),
        'min_marks':fields.float("Min Marks"),
        'obtain_marks':fields.float("Obtain Marks"),
        'max_marks':fields.float("Maximum Marks"),
        'grade':fields.selection([('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('f', 'F'), ], "Grade")
    }
    
class subject_subject(osv.osv):
    
    _name = 'subject.subject'
    
    _columns = {
        'code':fields.char("Code", size=4),
        'name':fields.char("Name", size=24),
    }
