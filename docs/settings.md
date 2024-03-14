## Settings

`JQUERY_URL`
:   jQuery 2.2.0 is loaded from Google's CDN if this is set to `True`. If you would prefer to
    use a different version put the full URL here. Set `JQUERY_URL = False`
    to disable loading jQuery altogether.

`USE_DJANGO_JQUERY`
:   By default, `smart_selects` loads jQuery from Google's CDN. However, it can use jQuery from Django's
    admin area. Set `USE_DJANGO_JQUERY = True` to enable this behaviour.

`SMART_SELECTS_CHECK_MODEL_PERMISSION`
:   By default, `smart_selects` does not check if the logged-in user has access to view the chained model permissions.
    Setting this option to `True` will cause `smart-selects` to check if the user has the view_model
    permission in the ajax endpoint.
