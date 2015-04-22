from osv import osv, fields

class sale_order(osv.osv):
    
    _inherit = 'sale.order'
    
    _columns = {
        'delivery_charges':fields.float("Delivery Charges"),
        'email':fields.char("Email", size=64),
        'contact':fields.char("Contact No.", size=14),
    }
    
    
