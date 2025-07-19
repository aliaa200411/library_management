from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class LibraryBorrowing(models.Model):
    _name = 'library.borrowing'
    _description = 'Borrowing Record'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.context_today)
    return_date = fields.Date(string='Return Date', store=True)
    returned = fields.Boolean(string='Returned', default=False)

    @api.onchange('borrow_date')
    def _onchange_borrow_date(self):
        if self.borrow_date:
            self.return_date = self.borrow_date + timedelta(days=7)

    @api.model
    def create(self, vals):
        book = self.env['library.book'].browse(vals['book_id'])
        if not book.is_available:
            raise ValidationError("This book is already borrowed and not available.")
        record = super(LibraryBorrowing, self).create(vals)
        book.write({'is_available': False})
        return record

    def action_mark_returned(self):
        for record in self:
            if not record.returned:
                record.returned = True
                book.write({'is_available': True})

    @api.constrains('book_id')
    def _check_duplicate_borrowing(self):
        for record in self:
            ongoing = self.search([
                ('book_id', '=', record.book_id.id),
                ('returned', '=', False),
                ('id', '!=', record.id)
            ])
            if ongoing:
                raise ValidationError("This book is already borrowed and has not been returned yet.")
