SECRET_KEY = 'django-insecure-@)($5h2+(*5^6qwj01m&l*s)_@3lqppj(j#ushke+9h4k0!8t@'

ALLOWED_HOSTS = ['127.0.0.1:99', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:99"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "fakecsv",
        "USER":"fakecsv",
        "PASSWORD":"fakecsvE1!",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
            }
    }
}