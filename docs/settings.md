## Settings

`JQUERY_URL`
:   jQuery 2.2.0 is loaded from Google's CDN if this is set to `True`. If you would prefer to
    use a different version put the full URL here. Set `JQUERY_URL = False`
    to disable loading jQuery altogether.

`USE_DJANGO_JQUERY`
:   By default, `smart_selects` loads jQuery from Google's CDN. However, it can use jQuery from Django's
    admin area. Set `USE_DJANGO_JQUERY = True` to enable this behaviour.

`SMART_SELECTS_SECURED_FILTERING`
:   By default, chaining will be prevented if the target model doesn't declare any chained fields in its model.
    This option can be disabled (for example if you want to chain only in forms), but please be aware of the security implications.
