from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_validate_delivery = fields.Boolean(string="Auto Validate Delivery on SO Confirmation", config_parameter="sale_auto_process.auto_validate_delivery")
    auto_invoice_action = fields.Selection([
        ('no', 'Do Nothing'),
        ('draft', 'Create Invoice'),
        ('post', 'Invoice and Posted'),
        ('paid', 'Post and Register Payment'),
    ], string="Auto Sale Invoice", config_parameter="sale_auto_process.auto_invoice_action", default='no')


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_confirm(self):
        res = super().action_confirm()

        auto_delivery = self.env['ir.config_parameter'].sudo().get_param('sale_auto_process.auto_validate_delivery') == 'True'
        auto_invoice_action = self.env['ir.config_parameter'].sudo().get_param('sale_auto_process.auto_invoice_action',
                                                                               default='no')

        for order in self:
            if auto_delivery:
                for picking in order.picking_ids:
                    if picking.state not in ['done', 'cancel']:
                        if picking.state == 'confirmed':
                            picking.action_assign()
                        if picking.state in ['assigned', 'waiting']:
                            picking.button_validate()

            if auto_invoice_action != 'no' and order.invoice_status in ['to invoice']:
                invoice = order._create_invoices()
                if auto_invoice_action in ['post', 'paid']:
                    invoice.action_post()
                if auto_invoice_action == 'paid':
                    for inv in invoice:
                        if inv.amount_residual > 0:
                            payment_register = self.env['account.payment.register'].with_context(
                                active_model='account.move',
                                active_ids=inv.ids
                            ).create({
                                'amount': inv.amount_residual,
                                'payment_date': fields.Date.today(),
                                'journal_id': self.env['account.journal'].search([('type', '=', 'bank')], limit=1).id,
                            })
                            payment_register.action_create_payments()

        return res
