from openerp.osv import fields, osv
from datetime import datetime,date
from openerp import workflow
from openerp import netsvc
wf_service = netsvc.LocalService('workflow')


class state_account_invoice(osv.osv):
    _inherit ='account.invoice'

    def state_invoice_validate(self, cr, uid, ids, context=None):
        invoice_ids = self.search(cr,uid,[('state','=','open')],context=context)
        res =[]
        for id in invoice_ids:
            print ":::::::::::::::::",invoice_ids
            wf_service.trg_validate(uid,'account.invoice', id, 'invoice_cancel',cr)
            self.action_cancel_draft(cr, uid, id, context=context)
            wf_service.trg_validate(uid,'account.invoice', id, 'invoice_open',cr)
        return res