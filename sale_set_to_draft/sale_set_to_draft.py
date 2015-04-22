# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################

from datetime import datetime, date
import time
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc


class sale_order(osv.osv):
    _inherit = 'sale.order'

    def action_set_draft(self, cr, uid, ids, *args):
       line_pool = self.pool.get('sale.order.line')
       cr.execute("update sale_order set state = 'draft' where id=%s", [ids[0],])
       wf_service = netsvc.LocalService("workflow")
       for sale_id in ids:
           wf_service.trg_delete(uid, 'sale.order', sale_id, cr)
           wf_service.trg_create(uid, 'sale.order', sale_id, cr)
       cr.execute("update sale_order_line set state = 'draft' where order_id=%s", [ids[0],])
       return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
