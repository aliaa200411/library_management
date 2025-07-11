{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'Manage books, authors, and borrowing in a library',
    'author': 'Aliaa Al_Troun',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/book_views.xml',
        'views/author_views.xml',
        'views/borrowing_views.xml',
        'views/library_menu.xml',

    ],
    'installable': True,
    'application': True,
}
