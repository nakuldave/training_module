# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#message_post(cr, uid, self.group_port_id, body='Message')
import time
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

from openerp.osv import osv, fields
from openerp import tools, SUPERUSER_ID
from openerp.tools.translate import _
from openerp import netsvc

class crm_lead(osv.osv):
    _inherit = 'crm.lead'

    def create(self, cr, uid, values, context=None):
        task_id = super(crm_lead, self).create(cr, uid, values, context=context)
        if context.get('search_default_partner_id',False):
            body='<b> Opportunity %s Created </b>'%(values.get('name',''))
            self.pool.get('res.partner').message_post(cr, uid, context.get('search_default_partner_id'), body=body)
        return task_id

    def case_mark_lost(self, cr, uid, ids, context=None):
        """ Mark the case as lost: state=cancel and probability=0 """
        for lead in self.browse(cr, uid, ids):
            body='<b> Opportunity %s.. Lost </b>'%(lead.name)
            stage_id = self.stage_find(cr, uid, [lead], lead.section_id.id or False, [('probability', '=', 0.0),('on_change','=',True)], context=context)
            if stage_id:
                self.pool.get('res.partner').message_post(cr, uid, context.get('search_default_partner_id'), body=body)
                self.case_set(cr, uid, [lead.id], values_to_update={'probability': 0.0}, new_stage_id=stage_id, context=context)
        return True
    
    def case_mark_won(self, cr, uid, ids, context=None):
        """ Mark the case as won: state=done and probability=100 """
        for lead in self.browse(cr, uid, ids):
            body='<b> Opportunity %s.. Won </b>'%(lead.name)
            stage_id = self.stage_find(cr, uid, [lead], lead.section_id.id or False, [('probability', '=', 100.0),('on_change','=',True)], context=context)
            if stage_id:
                self.pool.get('res.partner').message_post(cr, uid, context.get('search_default_partner_id'), body=body)
                self.case_set(cr, uid, [lead.id], values_to_update={'probability': 100.0}, new_stage_id=stage_id, context=context)
        return True
    def _lead_create_contact(self, cr, uid, lead, name, is_company, parent_id=False, context=None):
        partner = self.pool.get('res.partner')
        vals = {'name': name,
            'user_id': lead.user_id.id,
            'comment': lead.description,
            'section_id': lead.section_id.id or False,
            'parent_id': parent_id,
            'phone': lead.phone,
            'mobile': lead.mobile,
            'email': tools.email_split(lead.email_from) and tools.email_split(lead.email_from)[0] or False,
            'website':lead.website,
            'phone':lead.phone,
            'fax': lead.fax,
            'title': lead.title and lead.title.id or False,
            'function': lead.function,
            'street': lead.street,
            'street2': lead.street2,
            'zip': lead.zip,
            'city': lead.city,
            'country_id': lead.country_id and lead.country_id.id or False,
            'state_id': lead.state_id and lead.state_id.id or False,
            'is_company': is_company,
            'type': 'contact'
        }
        partner = partner.create(cr, uid, vals, context=context)
        return partner


    def _create_lead_partner(self, cr, uid, lead, context=None):
        partner_id = False
        if lead.partner_name and lead.contact_name:
            partner_id = self._lead_create_contact(cr, uid, lead, lead.partner_name, True, context=context)
            partner_id = self._lead_create_contact(cr, uid, lead, lead.contact_name, False, partner_id, context=context)
        elif lead.partner_name and not lead.contact_name:
            partner_id = self._lead_create_contact(cr, uid, lead, lead.partner_name, True, context=context)
        elif not lead.partner_name and lead.contact_name:
            partner_id = self._lead_create_contact(cr, uid, lead, lead.contact_name, False, context=context)
        elif lead.email_from and self.pool.get('res.partner')._parse_partner_name(lead.email_from, context=context)[0]:
            contact_name = self.pool.get('res.partner')._parse_partner_name(lead.email_from, context=context)[0]
            partner_id = self._lead_create_contact(cr, uid, lead, contact_name, False, context=context)
        elif lead.website:
            web = self._lead_create_contact(cr, uid, lead, lead.website, True, context=context)
            partner_id = self._lead_create_contact(cr, uid, lead, web, False, context=context)
        elif lead.phone:
            ph = self._lead_create_contact(cr, uid, lead, lead.phone, True, context=context)
            partner_id = self._lead_create_contact(cr, uid, lead, ph, False, context=context)

        else:
            raise osv.except_osv(
                _('Warning!'),
                _('No customer name defined. Please fill one of the following fields: Company Name, Contact Name or Email ("Name <email@address>")')
            )
        return partner_id


    _columns = {
        'skype': fields.char('Skype'),
        'website': fields.char('Website', size=64),
        'email_to': fields.char('Email2'),
    }
class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
    }

class crm_phonecall(osv.osv):
    _inherit = 'crm.phonecall'
    
    def create(self, cr, uid, values, context=None):
        task_id = super(crm_phonecall, self).create(cr, uid, values, context=context)
        if context.get('search_default_partner_id',False):
            body='<b> Phone call created for %s.. </b>'%(values.get('name',''))
            self.pool.get('res.partner').message_post(cr, uid, context.get('search_default_partner_id'), body=body)
        return task_id

    def action_button_convert2opportunity(self, cr, uid, ids, context=None):
        if len(ids) != 1:
            raise osv.except_osv(_('Warning!'),_('It\'s only possible to convert one phonecall at a time.'))
        opp = self.browse(cr, uid, ids[0], context=context)
        if opp.name:
            body='<b> Convet to Opprtunity %s</b>'%(opp.name)
            self.pool.get('res.partner').message_post(cr, uid, context.get('search_default_partner_id'), body=body)
        opportunity_dict = self.convert_opportunity(cr, uid, ids, context=context)
        return self.pool.get('crm.lead').redirect_opportunity_view(cr, uid, opportunity_dict[ids[0]], context)


class project_task(osv.osv):
    _inherit = 'project.task'
    
    def create(self, cr, uid, values, context=None):
        task_id = super(project_task, self).create(cr, uid, values, context=context)
        if context.get('search_default_partner_id'):
            body_partner='<b> Task %s Created </b>'%(values.get('name',''))
            self.pool.get('res.partner').message_post(cr, uid, context.get('search_default_partner_id'), body=body_partner)
            body='<b> Task %s Created </b>'%(values.get('name',''))
            print "\n\n>>>body",body,'\n\n>>>>context',context
            self.pool.get('crm.lead').message_post(cr, uid, context.get('active_id'), body=body)
        return task_id

    def action_close(self, cr, uid, ids, context=None):
        """ This action closes the task
        """
        task_id = len(ids) and ids[0] or False
        task_browse = self.browse(cr, uid, ids[0], context=context)
        self._check_child_task(cr, uid, ids, context=context)
        if task_browse.name:
            body='<b> Task %s Done </b>'%(task_browse.name)
            self.pool.get('res.partner').message_post(cr, uid, context.get('search_default_partner_id'), body=body)
        if task_browse.name:
            body='<b> Task %s Done </b>'%(task_browse.name)
            self.pool.get('crm.lead').message_post(cr, uid, context.get('active_id'), body=body)
        if not task_id: return False
        return self.do_close(cr, uid, [task_id], context=context)

    def do_cancel(self, cr, uid, ids, context=None):
        """ Compatibility when changing to case_cancel. """
        task_browse = self.browse(cr, uid, ids[0], context=context)
        if task_browse.name:
            body='<b> Task %s Cancelled </b>'%(task_browse.name)
            self.pool.get('res.partner').message_post(cr, uid, context.get('search_default_partner_id'), body=body)
        if task_browse.name:
            body='<b> Task %s Cancelled </b>'%(task_browse.name)
            self.pool.get('crm.lead').message_post(cr, uid, context.get('active_id'), body=body)
        return self.case_cancel(cr, uid, ids, context=context)


        
#class crm_meeting(osv.osv):
#    _inherit = 'crm.meeting'
#
#    def create(self, cr, uid, values, context=None):
#        task_id = super(crm_meeting, self).create(cr, uid, values, context=context)
#        if context.get('search_default_partner_ids',False):
#            body='<b> Meeting %s Created </b>'%(values.get('name',''))
#            self.pool.get('res.partner').message_post(cr, uid, context.get('search_default_partner_id'), body=body)
#        return task_id

class sale_order(osv.osv):
    _inherit = 'sale.order'
    def create(self, cr, uid, values, context=None):
        so_id = super(sale_order, self).create(cr, uid, values, context=context)
        body='<b> Sale ORder %s Created </b>'%(values.get('name',''))
        self.pool.get('res.partner').message_post(cr, uid, values.get('partner_id'), body=body)
        return so_id
    
    

        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
