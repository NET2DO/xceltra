from openerp import fields, models,api

class sale_order(models.Model):
    _inherit ='sale.order'

    @api.model
    def create(self, vals):
        res=super(sale_order,self).create(vals)
        if "Opportunity" in vals['origin']:
            op_id=[int(s) for s in vals['origin'].split() if s.isdigit()][0]
            for i in self.env['crm.lead'].browse(op_id):
                i.op_quotation=vals['name']
        return res
