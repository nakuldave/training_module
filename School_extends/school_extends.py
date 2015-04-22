from openerp.osv import fields,osv
from datetime import datetime,date
class school_school (osv.Model):
    
    _inherit ='student.student'
    _columns ={
               'gender':fields.selection([('male','Male'), ('female','Female')],"Gender"),
               'titel':fields.many2one('titel.titel','Titel')
               }
        
class titel_titel (osv.Model):

    _name = 'titel.titel'

    _columns = {
                'name':fields.char('Name')
                }
    
class sale_sale (osv.Model):
    
    _inherit = 'product.demo.category'
    
    _columns = {
                'parent_category':fields.selection([('all products','All Products'), ('all products/saleable','All Products/Saleable'),('consumeable', 'Consumeable')],"Parent Category")
                }