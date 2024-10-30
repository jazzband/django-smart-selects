## Installation

1. Install `django-smart-selects` using a tool like `pip`:

    ```console
    $ pip install django-smart-selects
    ```

2. Add `smart_selects` to your `INSTALLED_APPS`
3. Add the `smart_selects` urls into your project's `urls.py`. This is needed for the `Chained Selects` and `Chained ManyToMany Selects`. For example:

    ```python
    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^chaining/', include('smart_selects.urls')),
    )
    ```

4. You will also need to include jQuery in every page that includes a field from `smart_selects`, or set `Use USE_DJANGO_JQUERY = True` in your project's `settings.py`.
