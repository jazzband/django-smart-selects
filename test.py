if __name__ == '__main__':
    from django.conf import settings
    settings.configure(
        DATABASES={'default': {
            'NAME': ':memory:', 'ENGINE': 'django.db.backends.sqlite3'
        }},
        INSTALLED_APPS=('smart_selects',),
        MIDDLEWARE_CLASSES=(),
    )
    from django.core.management import call_command
    import django

    if django.VERSION[:2] >= (1, 7):
        django.setup()
    call_command('test', 'smart_selects')
