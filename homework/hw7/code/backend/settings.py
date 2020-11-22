from werkzeug.security import generate_password_hash

users = {
    'vova': generate_password_hash('123'),
    'max': generate_password_hash('1234'),
    'yarik': generate_password_hash('12345')
}

products = (
    {
        'id': 1,
        'name': 'Rice',
        'price': '$2',
        'quantity': 10
    },
    {
        'id': 2,
        'name': 'Rice',
        'price': '$2',
        'quantity': 10
    },
    {
        'id': 3,
        'name': 'Rice',
        'price': '$2',
        'quantity': 10
    },
)
