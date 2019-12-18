## Installation

1. Add `smart_selects` to your `INSTALLED_APPS`
2. Add the `smart_selects` urls into your project's `urls.py`. This is needed for the `Chained Selects` and `Chained ManyToMany Selects`. For example:

    ```python
    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^chaining/', include('smart_selects.urls')),
    )
    ```

3. You will also need to include jQuery in every page that includes a field from `smart_selects`, or set `JQUERY_URL = True` in your project's `settings.py`.
