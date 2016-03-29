from openerp import fields, models


class crm_lead(models.Model):
    _inherit = 'crm.lead'
    website_field = fields.Char(string='Website', size=256)
    lead_rate = fields.Many2one('crm.lead.rate', string='Rate')
    lead_category = fields.Many2one('crm.lead.category', string='Category')
    lead_status = fields.Many2one('crm.lead.states', string='States')
    lead_industry = fields.Many2one('crm.lead.industry', string='Industry')
    num_of_emp = fields.Char(string='Number Of Employees')
    annual_revenue = fields.Char(string='Annual revenue')


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
