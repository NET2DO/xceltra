from openerp import fields, models, api
import datetime


class crm_lead(models.Model):
    _inherit = 'crm.lead'
    website_field = fields.Char(string='Website', size=256)
    lead_rate = fields.Many2one('crm.lead.rate', string='Rate')
    lead_category = fields.Many2one('crm.lead.category', string='Category')
    lead_status = fields.Many2one('crm.lead.states', string='States')
    lead_industry = fields.Many2one('crm.lead.industry', string='Industry')
    num_of_emp = fields.Char(string='Number Of Employees')
    annual_revenue = fields.Char(string='Annual revenue')
    lead_source_lead = fields.Many2one('lead.source', string='Lead Source')


crm_lead()


class crm_lead_rate(models.Model):
    _name = 'crm.lead.rate'
    _rec_name = 'value'
    code = fields.Char(string='Code', required=True)
    value = fields.Char(string='Rate Value')


crm_lead_rate()


class crm_lead_category(models.Model):
    _name = 'crm.lead.category'
    _rec_name = 'name'
    code = fields.Char(string='Category Code', required=True)
    name = fields.Char(string='Category Name')


crm_lead_category()


class crm_lead_status(models.Model):
    _name = 'crm.lead.states'
    _rec_name = 'name'
    name = fields.Char(string='Lead Status')
    code = fields.Char(string='Status Code', required=True)


crm_lead_status()


class crm_lead_industry(models.Model):
    _name = 'crm.lead.industry'
    _rec_name = 'name'
    name = fields.Char(string='Lead Industry')
    code = fields.Char(string='Industry Code', required=True)


crm_lead_industry()


class crm_opportunities(models.Model):
    _inherit = 'crm.lead'
    op_sales_man = fields.Many2one('res.users', string='Sales Man')
    op_sales_manager = fields.Many2one('res.users', string='Sales Manger')
    code_seq = fields.Char('Sequence', readonly=True)
    account_name = fields.Char('Account Name')
    op_category_id = fields.Many2one('opportunities.category', string='Category')
    op_op_solution = fields.Many2one('opportunities.solution', string='Solution Type')
    track_number = fields.Char(compute='compute_track', string='Tracking number')
    op_type = fields.Many2one('opportunities.type', string='Type')

    enquiry_date = fields.Date(string='Enquiry Date')
    expected_close = fields.Date(compute='get_the_date', string='Expected Closing ')
    op_refe = fields.Text(string='Referance')
    op_project = fields.Many2one('project.project', string='Project')
    close_note = fields.Text(string='Close Note')
    follow_up_note = fields.Text(string='Follow Up Note')
    op_quotation = fields.Char(string='Quotation Name')

    @api.model
    def create(self, vals):
        vals.update({'code_seq': self.env['ir.sequence'].get('opportunities.opportunities')})
        res = super(crm_opportunities, self).create(vals)
        return res

    @api.multi
    @api.onchange('partner_id')
    def on_change_partner_ids(self):
        if self.partner_id:
            partner = self.env['res.partner'].browse(self.partner_id.id)
            self.name = partner.name

    @api.depends('create_date')
    def get_the_date(self):
        for i in self:
            if i.create_date:
                i.expected_close = str(
                    datetime.datetime.strptime(i.create_date, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=30))

    @api.depends('code_seq', 'partner_id', 'partner_id.country_id')
    def compute_track(self):
        my_code = ''
        my_first_cus = ''
        for i in self:
            if not i.code_seq and i.partner_id and i.partner_id.country_id:
                first_letter_of_customer = i.partner_id.name[0]
                first_letter_of_country = i.partner_id.country_id.name[0]
                i.track_number = my_code + first_letter_of_customer + first_letter_of_country
            elif i.code_seq and i.partner_id and i.partner_id.country_id:
                first_letter_of_customer = i.partner_id.name[0]
                first_letter_of_country = i.partner_id.country_id.name[0]
                i.track_number = i.code_seq + first_letter_of_customer + first_letter_of_country
            elif not i.partner_id and i.code_seq and i.partner_id.country_id:
                first_letter_of_country = i.partner_id.country_id.name[0]
                i.track_number = i.code_seq + my_first_cus + first_letter_of_country
            elif not i.partner_id and not i.code_seq and i.partner_id.country_id:
                first_letter_of_country = i.partner_id.country_id.name[0]
                i.track_number = my_code + my_first_cus + first_letter_of_country
            elif i.partner_id and i.code_seq and not i.partner_id.country_id:
                i.track_number = my_code + my_first_cus + ''
            elif not i.partner_id and not i.code_seq and not i.partner_id.country_id:
                i.track_number = my_code + my_first_cus + ''
            elif i.partner_id and not i.code_seq and not i.partner_id.country_id:
                first_letter_of_customer = i.partner_id.name[0]
                i.track_number = my_code + first_letter_of_customer + ''
            elif not i.partner_id and i.code_seq and not i.partner_id.country_id:
                i.track_number = i.code_seq + my_first_cus + ''


crm_opportunities()


class opportunities_category(models.Model):
    _name = 'opportunities.category'
    _rec_name = 'name'
    name = fields.Char(string='Category Name')
    code = fields.Char(string='Category Code', required=True)


opportunities_category()


class opportunities_solution(models.Model):
    _name = 'opportunities.solution'
    _rec_name = 'name'
    name = fields.Char(string='Solution Name')
    code = fields.Char(string='Solution Code ', required=True)
    sub_soluation_categ = fields.One2many('opportunities.solution.sub', 'line_id', string='Sub Category')


opportunities_solution()


class opportunities_solution_categ(models.Model):
    _name = 'opportunities.solution.sub'
    _rec_name = 'name'
    line_id = fields.Many2one('opportunities.solution')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


opportunities_solution_categ()


class lead_source(models.Model):
    _name = 'lead.source'
    _rec_name = 'name'
    name = fields.Char(string='Source Name')
    code = fields.Char(string='Source Code ', required=True)
    lead_details = fields.One2many('lead.source.sub', 'line_id', string='Source details ')


lead_source()


class lead_source_sub(models.Model):
    _name = 'lead.source.sub'
    _rec_name = 'name'
    line_id = fields.Many2one('lead.source')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


lead_source_sub()


class opportunities_type(models.Model):
    _name = 'opportunities.type'
    _rec_name = 'name'
    name = fields.Char(string='Type Name')
    code = fields.Char(string='Code', required=True)


opportunities_type()
