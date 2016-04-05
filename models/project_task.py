from openerp import models, fields
from datetime import datetime, timedelta

AVAILABLE_PRIORITIES = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High'),
]


class project_task(models.Model):
    _inherit = 'project.task', 'mail.thread'

    task_op_name = fields.Char(string='Opportunity Name')
    reminder = fields.Datetime(string='Reminder')
    feedback_text = fields.Text(string='Feedback')
    date_add = fields.Date(string='Date')
    edit_by = fields.Many2one('res.users', string='Edited By')
    priority = fields.Selection([
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High'),
        ('4', 'Very High'), ], string='Priority', default='2')

    def mail_remainder(self, cr, uid, context=None):
        next_day = datetime.now() + timedelta(days=1)
        project_task_objec = self.pool.get('project.task').search(cr, uid, [('reminder', '<=', next_day)])
        for rec in project_task_objec:
            for i in self._get_followers(cr, uid, rec, None, None, context=context):
                self.send_email_task(cr, uid, i, context)

    def send_email_task(self, cr, uid, partner, context=None):
        email = self.pool.get('res.partner').browse(cr, uid, partner.partner_id.id).email
        email_template_obj = self.pool.get('email.template')
        template_ids = email_template_obj.search(cr, uid, [('name', '=', 'Task Reminder alert')], context=context)
        email_template_obj.write(cr, uid, template_ids, {'email_to': email}, context)
        if template_ids:
            values = email_template_obj.generate_email(cr, uid, template_ids[0], partner.partner_id.id, context=context)
            mail_mail_obj = self.pool.get('mail.mail')
            msg_id = mail_mail_obj.create(cr, uid, values, context=context)
            if msg_id:
                mail_mail_obj.send(cr, uid, [msg_id], context=context)
        return True


project_task()
