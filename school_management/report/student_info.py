from openerp.report import report_sxw

report_sxw.report_sxw('report.student.info.rml', 'student.student',
                      "school_management/report/student_info.rml",
                      header="False")