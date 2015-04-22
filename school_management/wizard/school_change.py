from openerp.osv import osv, fields

class school_change_wizard(osv.osv_memory):
    
    _name = 'school.school.wizard'
    
    _columns = {
        'school_id':fields.many2one("school.school", "School"),
        'contact': fields.char("Contact No")
               }
    
    def change_contact(self, cr, uid, ids, context=None):
        
        school_obj = self.pool.get('school.school')
        for rec in self.browse(cr, uid, ids, context=context):
            if rec.school_id and rec.contact:
                vals = {'contact':rec.contact}
                school_obj.write(cr, uid, [rec.school_id.id], vals,context=context)
        return True