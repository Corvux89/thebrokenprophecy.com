def get_csp():
    csp = {
        'default-src': [
            '\'self\'',
            'https://docs.google.com',
            'https://code.jquery.com/'
            'https://cdn.jsdelivr.net/npm/',
            'https://www.googletagmanager.com/',
            'https://analytics.google.com/',
            'https://www.google-analytics.com/',
            'https://use.fontawesome.com',
            'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/bootstrap-icons.css',
            'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/fonts/',
        ],
        'script-src': [
            '\'self\'',
            'https://cdn.jsdelivr.net/',
            'https://www.googletagmanager.com/',
            'https://ajax.googleapis.com',
            'https://cdnjs.cloudflare.com/',
            'https://cdn.datatables.net/1.13.1/js/jquery.dataTables.js'
        ],
        'img-src': [
            '*',
            'data:'
        ],
        'style-src': [
            '\'self\'',
            'https://cdn.jsdelivr.net/',
            'https://use.fontawesome.com',
            'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/bootstrap-icons.css',
            'https://cdn.datatables.net/1.13.1/css/jquery.dataTables.css'
        ],
        'script-src-elem': [
            '\'self\'',
            'https://cdnjs.cloudflare.com/',
            'https://cdn.jsdelivr.net/',
            'https://ajax.googleapis.com',
            'https://cdn.datatables.net/1.13.1/js/jquery.dataTables.js'
        ]
    }

    return csp