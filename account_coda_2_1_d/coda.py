##############################################################################
#
# Copyright (c) 2004-2006 TINY SPRL. (http://tiny.be) All Rights Reserved.
#                    Fabien Pinckaers <fp@tiny.Be>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import time
from osv import osv,fields

class account_coda(osv.osv):
    _name = "account.coda"
    _description = "CODA Format For Account"
    _columns = {
        'name': fields.binary('Coda File', readonly=True),
        #'statement_ids': fields.one2many('account.bank.statement','coda_id','Generated Bank Statement', readonly=True),
        'statement_id': fields.many2one('account.bank.statement','Generated Bank Statement', select=True,readonly=True),
        'note': fields.text('Import Log', readonly=True),
        'journal_id': fields.many2one('account.journal','Bank Journal', readonly=True,select=True),
        'date': fields.date('Import Date', readonly=True,select=True),
        'user_id': fields.many2one('res.users','User', readonly=True, select=True),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'user_id': lambda self,cr,uid,context: uid,
    }
account_coda()

class account_bank_statement(osv.osv):
    _inherit = "account.bank.statement"
    _columns = {
        'coda_id':fields.many2one('account.coda','Coda'),
    }
account_bank_statement()

class account_bank_statement_line(osv.osv):
    _inherit = "account.bank.statement.line"
    _columns = {
       'statement_id': fields.many2one('account.bank.statement', 'Statement',
            select=True, required=True,ondelete='cascade'),
    }
account_bank_statement_line()
