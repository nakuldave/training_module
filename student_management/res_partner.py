from osv import osv, fields

class res_partner(osv.osv):
    
    _inherit = 'res.partner'

    def name_get(self, cr, uid, ids, context=None):
        
        print "Inside the Name Get method..." 
        res = super(res_partner, self).name_get(cr, uid, ids, context=context)
        
        final_result = []
        partner_ids = []
        if ids:
            if isinstance(ids, int):
                partner_ids.append(ids)
            elif isinstance(ids, list):
                partner_ids += ids
            for partner in self.browse(cr, uid, partner_ids, context=context):
                partner_data = partner.name or ""
                partner_data += " ["
                partner_data += partner.ref or ""
                partner_data += "]"
                final_result.append((partner.id, partner_data))
            return final_result
            
        return res
    
    
#     def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        res = super(res_partner, self).name_search(cr, user, name=name, args=args, operator=operator, context=context, limit=limit)

        return res
