from openerp import fields, models, api
import time
import datetime


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.depends('name', 'create_date', 'origin')
    def get_the_name(self):
        for i in self:
            if i.create_date and i.origin and i.name:
                date_mine = str(datetime.datetime.strptime(i.create_date, '%Y-%m-%d %H:%M:%S').date())
                if "Opportunity" in i.origin:
                    op_id = [int(s) for s in i.origin.split() if s.isdigit()][0]
                    i.quot_name = self.env['crm.lead'].browse(op_id).name + \
                                  ' - ' + date_mine + ' - ' + i.name

    quot_name = fields.Char(compute='get_the_name', string='Quotation Name')
    branch_id = fields.Many2one('quot.branch', string='Branch')
    branch_address = fields.Char(string='Branch Address', related='branch_id.branch_address')
    issue_date = fields.Date(string='Issue Date', default=time.strftime('%Y-%m-%d'))
    valid_until = fields.Datetime(string='Validate Until', default=str(
        datetime.datetime.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d') + datetime.timedelta(days=30)))
    quot_works = fields.Char(string='XWroks')
    sales_terms = fields.Text(string='Sales terms')
    bank_account = fields.Char(string='Bank Account', related='branch_id.branch_address')
    lead_time = fields.Char(string='Lead Time')
    convert_to=fields.Many2one('res.currency',string='Convert To')

    @api.model
    def create(self, vals):
        res = super(sale_order, self).create(vals)
        if vals['origin']:
            if "Opportunity" in vals['origin']:
                op_id = [int(s) for s in vals['origin'].split() if s.isdigit()][0]
                for i in self.env['crm.lead'].browse(op_id):
                    i.op_quotation = vals['name']
        return res


sale_order()


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    cost_price_readonly = fields.Char(string='Cost Price', readonly=True)
    cost_price_not = fields.Char(string='Cost Price')
    reason = fields.Text(string='Reason')
    discount = fields.Float(string='Discount')
    supplier_pro = fields.Many2one('res.partner', string='Supplier')
    lead_time = fields.Char(string='Lead Time', related='order_id.lead_time')


sale_order_line()


class quot_branch(models.Model):
    _name = 'quot.branch'
    _rec_name = 'name'
    name = fields.Char(string='Branch Name')
    code = fields.Char(string='Branch Code', required=True)
    branch_address = fields.Char(string='Branch Address')


quot_branch()
