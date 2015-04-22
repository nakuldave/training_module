from openerp.osv import fields,osv
from datetime import datetime, timedelta

class product_uomdemo (osv.Model):

    _name = 'product.uomdemo'
    
    _columns ={
                'name':fields.char('Name'),
                'code':fields.char('Code'),
               }

class product_demo_category (osv.Model):

    _name = 'product.demo.category'
    
    _columns ={
                'name':fields.char('Name'),
                'code':fields.char('Code'),
               }

class product_demo (osv.Model):
    
    def create(self, cr, uid, vals, context=None):
        res = {}
        if not vals.get('barcode'):
            vals.update({'barcode':vals.get('name')})
        return super(product_demo, self).create(cr, uid, vals, context=context)
    

    _name = 'productdemo.productdemo'
    
    _columns ={
                'image':fields.binary("Image"),
                'name':fields.char('Name'),
                'cat_id':fields.many2one('product.demo.category',"Category"),
                'unit_price':fields.float('Sale Price'),
                'uom_id':fields.many2one('product.uomdemo','Unit Type'),
                'product_type':fields.selection([('consumable', 'Consumable'), ('service', 'Service')], string="Product Type"),
                'internal_ref':fields.char('Internal Reference'),
                'barcode': fields.char('EAN 13 Barcode'),
                'sale_ok': fields.boolean('Can be Sold')
               }

class sale_sale (osv.Model):
    
    _name = 'sale.sale'

    status_selection = [('draft', 'Draft'),
                        ('confirm', 'Sale Order'),
                        ('done', 'Done')]
    
    def confirm_sale(self, cr, uid, ids, context=None):
        next_sequence = self.pool.get('ir.sequence').get(cr, uid, 'saleorder.code')
        self.write(cr, uid, ids, {'state':"confirm",'name':next_sequence}, context=context)
        return True

    def set_to_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':"done"}, context=context)
        return True 

    def set_to_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':"draft"}, context=context)
        return True 
    
    def untax_subtotal(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        for rec in self.browse(cr, uid, ids, context=context):
            total_amount = 0.0
            for line in rec.order_line_ids:
                total_amount += line.sub_total
            res[rec.id] = total_amount
        return res

    
    _columns ={
               'name':fields.char('Name'),
               'customer_id':fields.many2one('res.partner','Customer'),
               'date': fields.date("Date"),
               'customer_ref': fields.char("Customer Reference"),
               'state':fields.selection(status_selection, "State"),
               'order_line_ids':fields.one2many('sale.sale.line','sale_id',"Order Lines"),
               'total': fields.function (untax_subtotal, type ='float', string='Total')
               }
    
    _defaults = {
        'state':'draft',
        'date': fields.date.context_today
                }
    
class sale_sale_line (osv.Model):

    _name = 'sale.sale.line'
    
    def _sub_total(self, cr, uid, ids, fields, arg, context=None):

        res={}
        for record in self.browse(cr, uid, ids,context=context):
            res[record.id]=record.unit_price*record.qty
        return res
    
    def get_productdetails(self, cr, uid, ids,product_id,context=None):
        
        res = {}
        if product_id:
            partner_rec = self.pool.get('productdemo.productdemo').browse(cr, uid, product_id, context=context)
            res = {'value':{'name': partner_rec.name or '',
                            'unit_price': partner_rec.unit_price or 0.0,
                            'uom_id': partner_rec.uom_id and partner_rec.uom_id.id or False
                            }}
        return res
    _columns = {
                'sale_id': fields.many2one('sale.sale','Sale'),
                'product_id': fields.many2one('productdemo.productdemo','Product'),
                'name':fields.char('Description'),
                'unit_price':fields.float('Price'),
                'qty':fields.integer('quantity'),
                'uom_id':fields.many2one('product.uomdemo','Unit Type'),
                'sub_total':fields.function(_sub_total, type='float',string='Sub Total'),
               }
    
    _defaults = {
        'qty': 1.0
                }

class product_demo_category (osv.Model):

    _name = 'product.demo.category'
    
    _columns ={
                'name':fields.char('Name'),
                'code':fields.char('Code'),
               }