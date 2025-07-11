from odoo import models, fields,api

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(string='Name', required=True)
    biography = fields.Text(string='Biography')  
    birth_date = fields.Date(string='Date of Birth') 
    nationality = fields.Char(string='Nationality')
    email = fields.Char(string='Email')
    book_ids = fields.One2many('library.book', 'author_id', string='Books')
