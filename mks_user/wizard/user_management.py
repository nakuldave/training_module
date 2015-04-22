import time
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from osv import fields, osv
from openerp.tools import ustr
from openerp.tools.translate import _
from openerp import tools
from openerp import SUPERUSER_ID

class res_users(osv.osv):
    _inherit = "res.users"
    
    def create(self, cr, uid, values, context=None):
        res = super(res_users, self).create(cr, uid, values, context)
        cr.execute("insert into res_groups_users_rel values (%d,%d)" % (res,values['role_type_id']))
        return res
    
    _columns = {
                #'name' : fields.char('First Name',required=True),
                'l_name' : fields.char('Last Name',required=True),
                'u_mail' : fields.char('Email Address',required=True),
        
        'role_type_id': fields.many2one('res.groups', 'User Type',required=True),
        'user_settings': fields.boolean('Open User Settings'),
        'password': fields.char('Password', size=64, 
            help="Keep empty if you don't want the user to be able to connect on the system."),
        
        # Special behavior for this field: res.company.search() will only return the companies
        # available to the current user (should be the user's companies?), when the user_preference
        # context is set.
 
        
    }
    
   
    
    
    
    def create_user_button(self, cr, uid, ids,vals, context=None):
        f_name = ''
        for obj in self.browse(cr,uid,ids,context):
            f_name = obj.name + ' ' + obj.l_name
            self.write(cr, uid, ids, {'name':f_name,'user_email':obj.u_mail}, context)

        return True

    def button_redirect(self, cr, uid, ids, context=None):
        f_name = ''
        for obj in self.browse(cr,uid,ids,context):
            f_name = obj.name + ' ' + obj.l_name
            self.write(cr, uid, ids, {'name':f_name,'user_email':obj.u_mail}, context)
            
    def onchange_user_view(self, cr, uid, ids, user_settings, context=None):

        res = {}
        if user_settings:
            partner_rec = self.pool.get('res.users').browse(cr, uid, user_settings, context=context)
            res = {'value':{'user_settings': partner_rec.base.view_users_tree
                            }}

        return {
                'name': 'Users',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.pool.get('ir.ui.view').search(cr, uid, [('name','=','res.users.form')])[0],
                'res_model': 'res.users',
                'res_id': ids[0],
                'type': 'ir.actions.act_window',
                'res_id': self_obj.sale_order_id.id,
                'target': 'new',
                'context': context,
                'nodestroy': True,
        }

res_users()



class res_groups(osv.osv):
    _inherit = "res.groups"
    
    _columns = {
                #'name' : fields.char('First Name',required=True),
                'is_true' : fields.boolean('Is User Type'),
                }
    
res_groups()

# class groups_view(osv.osv):
#     _inherit = "res.groups"
#  
#     def create(self, cr, uid, values, context=None):
#         res = super(groups_view, self).create(cr, uid, values, context)
#         self.update_user_groups_view(cr, uid, context)
#         return res
#     
#     def get_user_groups_view(self, cr, uid, context=None):
#             try:
#                 view = self.pool.get('ir.model.data').get_object(cr, SUPERUSER_ID, 'base', 'user_groups_view_new', context)
#                 print "in my group view"
#                 assert view and view._table_name == 'ir.ui.view'
#             except Exception:
#                 view = False
#             return view
#    
# groups_view()