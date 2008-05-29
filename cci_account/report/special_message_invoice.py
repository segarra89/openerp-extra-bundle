##############################################################################
#
# Copyright (c) 2005-2006 TINY SPRL. (http://tiny.be) All Rights Reserved.
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
from report import report_sxw
import pooler
parents = {
    'tr':1,
    'li':1,
    'story': 0,
    'section': 0
    }

class account_invoice_with_message(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
		super(account_invoice_with_message, self).__init__(cr, uid, name, context)
		self.localcontext.update({
			'time': time,
			'spcl_msg': self.spcl_msg,
			'invoice_lines': self.invoice_lines,
            'repeat_In':self.repeat_In,
            'find_vcs' : self.find_vcs

		})
		self.context = context

    def find_vcs(self,invoice_id):
        item = pooler.get_pool(self.cr.dbname).get('account.invoice').browse(self.cr,self.uid,invoice_id)
        vcs =''
        if item.number:
            vcs3=str(item.number).split('/')[1]
            vcs1='0'+ str(item.date_invoice[2:4])
            if len(str(vcs3))>=5:
                vcs2=str(item.number[3]) + str(vcs3[0:5])
            elif len(str(vcs3))==4:
                vcs2=str(item.number[3]) + '0' +str(vcs3)
            else:
                vcs2=str(item.number[3]) + '00' +str(vcs3)

            vcs4= vcs1 + vcs2 + '0'

            vcs5=int(vcs4)
            check_digit=vcs5%97

            if check_digit==0:
                check_digit='97'
            if check_digit<=9:
                check_digit='0'+str(check_digit)
            vcs=vcs1+'/'+vcs2+'/'+ '0' +str(check_digit)
        return vcs

    def repeat_In(self, lst, name, nodes_parent=False,td=False,width=[],value=[],type=[]):
		self._node.data = ''
		node = self._find_parent(self._node, nodes_parent or parents)
		ns = node.nextSibling

		value=['tax_types','quantity','uos','price_unit','discount','price_subtotal','currency']
		type=['string','string','string','string','string','string','string']
		width=[62,42,20,62,51,50,24]
		td=7

		tableFlag=0

		if not lst:
		    lst.append(1)
		for ns in node.childNodes :
		    if tableFlag==1:
		        break
		    if ns and ns.nodeName!='#text' and ns.tagName=='blockTable' and td :
		        tableFlag=1

		        width_str = ns._attrs['colWidths'].nodeValue
		        ns.removeAttribute('colWidths')
		        total_td = td * len(value)

		        if not width:
		            for v in value:
		                width.append(30)
		        for v in range(len(value)):
		            width_str +=',%d'%width[v]

		        ns.setAttribute('colWidths',width_str)

		        child_list =  ns.childNodes

		        for child in child_list:
		            if child.nodeName=='tr':
		                lc = child.childNodes[1]
		#                        for t in range(td):
		                i=0
		                for v in value:
		                    t2="[[%s['type']=='text' and removeParentNode('tr')]]"%(name)
		                    t1= "[[ %s['%s'] ]]"%(name,v)
		                    t3="[[ %s['type']=='subtotal' and ( setTag('para','para',{'fontName':'Times-bold'})) ]]"%name
		                    newnode = lc.cloneNode(1)

		                    newnode.childNodes[1].lastChild.data = t1 + t2 +t3
		#                           newnode.childNodes[1].lastChild.data=[[ a['status']==1 and ( setTag('para','para',{'fontName':'Times-bold'})) ]]
		                    child.appendChild(newnode)
		                    newnode=False
		                    i+=1

		return super(account_invoice_with_message,self).repeatIn(lst, name, nodes_parent=False)
    def spcl_msg(self, form):
		account_msg_data = pooler.get_pool(self.cr.dbname).get('notify.message').browse(self.cr, self.uid, form['message'])
		msg = account_msg_data.msg
		return msg
    def invoice_lines(self,invoice):
		result =[]
		sub_total={}
		info=[]
		invoice_list=[]
		res={}
		list_in_seq={}
		ids = self.pool.get('account.invoice.line').search(self.cr, self.uid, [('invoice_id', '=', invoice.id)])
		ids.sort()
		for id in range(0,len(ids)):
		    info = self.pool.get('account.invoice.line').browse(self.cr, self.uid,ids[id], self.context.copy())
		    list_in_seq[info]=info.sequence
		#            invoice_list +=[info]
		i=1
		j=0
		final=sorted(list_in_seq.items(), lambda x, y: cmp(x[1], y[1]))
		invoice_list=[x[0] for x in final]
		sum_flag={}
		sum_flag[j]=-1
		for entry in invoice_list:
		    res={}

		    if entry.state=='article':
		        self.cr.execute('select tax_id from account_invoice_line_tax where invoice_line_id=%d'%(entry.id))
		        tax_ids=self.cr.fetchall()

		        if tax_ids==[]:
		            res['tax_types']=''
		        else:
		            tax_names_dict={}
		            for item in range(0,len(tax_ids))    :
		                self.cr.execute('select name from account_tax where id=%d'%(tax_ids[item][0]))
		                type=self.cr.fetchone()
		                tax_names_dict[item] =type[0]
		            tax_names = ','.join([tax_names_dict[x] for x in range(0,len(tax_names_dict))])
		            res['tax_types']=tax_names
		        res['name']=entry.name
		        res['quantity']="%.2f"%(entry.quantity)
		        res['price_unit']="%.2f"%(entry.price_unit)
		        res['discount']="%.2f"%(entry.discount)
		        res['price_subtotal']="%.2f"%(entry.price_subtotal)
		        sub_total[i]=entry.price_subtotal
		        i=i+1
		        res['note']=entry.note
		        res['currency']=invoice.currency_id.code
		        res['type']=entry.state

		        if entry.uos_id.id==False:
		            res['uos']=''
		        else:
		            uos_name = self.pool.get('product.uom').read(self.cr,self.uid,entry.uos_id.id,['name'])
		            res['uos']=uos_name['name']
		    else:

		        res['quantity']=''
		        res['price_unit']=''
		        res['discount']=''
		        res['tax_types']=''
		        res['type']=entry.state
		        res['note']=entry.note
		        res['uos']=''

		        if entry.state=='subtotal':
		            res['name']=entry.name
		            sum=0
		            sum_id=0
		            if sum_flag[j]==-1:
		                temp=1
		            else:
		                temp=sum_flag[j]

		            for sum_id in range(temp,len(sub_total)+1):
		                sum+=sub_total[sum_id]
		            sum_flag[j+1]= sum_id +1

		            j=j+1
		            res['price_subtotal']="%.2f"%(sum)
		            res['currency']=invoice.currency_id.code
		            res['quantity']=''
		            res['price_unit']=''
		            res['discount']=''
		            res['tax_types']=''
		            res['uos']=''
		        elif entry.state=='title':
		            res['name']=entry.name
		            res['price_subtotal']=''
		            res['currency']=''
		        elif entry.state=='text':
		            res['name']=entry.name
		            res['price_subtotal']=''
		            res['currency']=''
		        elif entry.state=='line':
		            res['quantity']='____________'
		            res['price_unit']='______________'
		            res['discount']='____________'
		            res['tax_types']='_________________'
		            res['uos']='_____'
		            res['name']='________________________________________'
		            res['price_subtotal']='_______________________'
		            res['currency']='_______'
		        elif entry.state=='break':
		            res['type']=entry.state
		            res['name']=entry.name
		            res['price_subtotal']=''
		            res['currency']=''
		        else:
		            res['name']=entry.name
		            res['price_subtotal']=''
		            res['currency']=invoice.currency_id.code

		    result.append(res)
		return result

report_sxw.report_sxw('report.cci_account.invoice', 'account.invoice', 'addons/cci_account/report/special_message_invoice.rml', parser=account_invoice_with_message)