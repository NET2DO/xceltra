from openerp import models, fields

AVAILABLE_PRIORITIES = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High'),
]


class project_task(models.Model):
    _inherit = 'project.task'
    task_op_name=fields.Char(string='Opportunity Name')
    task_priority = fields.Selection([
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High'),
        ('4', 'Very High'),], string='Priority',default='2')
