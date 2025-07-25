from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random

class LibraryMembership(models.Model):
    _name = 'library.membership'
    _description = 'Library Membership Request'

    partner_id = fields.Many2one(
        'res.partner',
        string='Member',
        required=True,
        domain="[('is_library_member','=',False)]"
    )
    registration_date = fields.Date(string="Registration Date", default=fields.Date.today)
    end_date = fields.Date(string="End Date")
    card_id = fields.Char(string="Card ID", readonly=True)
    payment_terms = fields.Selection([
        ('cash', 'Cash'),
        ('installment', 'Installment'),
    ], string="Payment Terms", default='cash')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('active', 'Active'),
    ], default='draft', string="Status")

    membership_lines = fields.One2many('library.membership.line', 'membership_id', string='Membership Lines')

    def action_confirm(self):
        for rec in self:
            if not rec.membership_lines:
                raise ValidationError("You must add at least one membership line before confirming.")
            rec.state = 'confirmed'

    def action_mark_paid(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise ValidationError("Membership must be confirmed before marking as paid.")
            rec.state = 'paid'
            rec.card_id = 'CARD-' + str(random.randint(1000, 9999))
            rec.partner_id.card_id = rec.card_id
            rec.partner_id.is_library_member = True

    def action_activate_membership(self):
        for rec in self:
            if rec.state != 'paid':
                raise ValidationError("Membership must be paid before activation.")
            rec.state = 'active'
