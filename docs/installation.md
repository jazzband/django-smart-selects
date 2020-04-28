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
