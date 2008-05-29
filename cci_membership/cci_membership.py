##############################################################################
#
# Copyright (c) 2004 TINY SPRL. (http://tiny.be) All Rights Reserved.
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

import netsvc
from osv import fields, osv

class res_partner(osv.osv):
    _inherit = 'res.partner'
    _description = 'Partner'
    def _membership_vcs(self,cr,uid,ids,field_name=None,arg=None,context={}):
        '''To obtain the ID of the partner in the form of a belgian VCS for a membership offer'''
        res = {}
        for id in ids:
            value_digits = 1000000000 + id
            check_digits = value_digits % 97
            if check_digits == 0:
                check_digits = 97
            pure_string = str(value_digits) +  ( str(check_digits).zfill(2) )
            res[id] = '***' + pure_string[0:3] + '/' + pure_string[3:7] + '/' + pure_string[7:] + '***'
        return res

    _columns = {
        'membership_vcs': fields.function( _membership_vcs, method=True,string='VCS number for membership offer', type='char', size=20)
                }

res_partner()