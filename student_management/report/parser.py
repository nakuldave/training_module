from report import report_sxw

class Student_Parser(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):

        super(Student_Parser, self).__init__(cr, uid, name, context=context)
        
        self.localcontext.update({
                                  'hello':self.hello_all,
                                  'serial':self.get_serial,
                                  'get_souda':self.get_subtotal,
                                })
        
    def get_subtotal(self, qty, unit_price):
        
        total = qty * unit_price
        return total
    
    def hello_all(self):
        
        return "Hello All, How are you?"

    def get_serial(self, order_line):
         
        serial_list = []
        counter = 1
        for data in order_line:
            serial_list.append(counter)
            counter += 1
            
        print "serial_list :::::::::::::", serial_list
        return serial_list

report_sxw.report_sxw('report.student.info.rep', 'student.student', 'addons/student_management/report/student_info.rml' , parser=Student_Parser, header=False)
report_sxw.report_sxw('report.sale.order.rep', 'sale.order', 'addons/student_management/report/sale_order_info.rml' , parser=Student_Parser, header=False)
report_sxw.report_sxw('report.sale.order.rep.webkit', 'sale.order', 'addons/student_management/report/order.mako' , parser=Student_Parser, header=False)
