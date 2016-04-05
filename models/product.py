from openerp import fields,models


class product_templete(models.Model):
    _inherit='product.template'
    min_quan=fields.Float(string='Min. Quantity',default=0.0)
    not_released=fields.Float(string='Not released',default=0.0)
product_templete()