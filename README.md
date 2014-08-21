Django Smart Selects
====================


Chained Selects
---------------

If you have the following model:

	class Location(models.Model)
		continent = models.ForeignKey(Continent)
		country = models.ForeignKey(Country)
		area = models.ForeignKey(Area)
		city = models.CharField(max_length=50)
		street = models.CharField(max_length=100)
		
And you want that if you select a continent only the countries are available that are located on this continent and the same for areas
you can do the following:

    from smart_selects.db_fields import ChainedForeignKey 

	class Location(models.Model)
		continent = models.ForeignKey(Continent)
		country = ChainedForeignKey(
			Country, 
			chained_field="continent",
			chained_model_field="continent", 
			show_all=False, 
			auto_choose=True
		)
		area = ChainedForeignKey(Area, chained_field="country", chained_model_field="country")
		city = models.CharField(max_length=50)
		street = models.CharField(max_length=100)
	
This example asumes that the Country Model has a continent = ForeignKey(Continent) field
and that the Area model has country = ForeignKey(Country) field.

- The chained field is the field on the same model the field should be chained too.
- The chained model field is the field of the chained model that corresponds to the model linked too by the chained field.
- show_all indicates if only the filtered results should be shown or if you also want to display the other results further down.
- auto_choose indicates that if there is only one option if it should be autoselected.

Grouped Selects
---------------

If you have the following model:

	class Location(models.Model)
		continent = models.ForeignKey(Continent)
		country = models.ForeignKey(Country)
		
And you want that all countries are grouped by the Continent and that <opt> Groups are used in the select change to the following:

    from smart_selects.db_fields import GroupedForeignKey
	
	class Location(models.Model)
		continent = models.ForeignKey(Continent)
		country = GroupedForeignKey(Country, "continent")
		
This example assumes that the Country Model has a foreignKey to Continent named "continent"
finished.
	


Installation
------------

1. Add "smart\_selects" to your INSTALLED\_APPS
2. Bind the `smart_selects` urls.py into your main urls.py with something like: `url(r'^chaining/', include('smart_selects.urls')),`
   This is needed for the chained-selects.
3. Profit


Settings
--------

`USE_DJANGO_JQUERY`
:   By default, `smart_selects` will use the bundled jQuery from Django 1.2's
    admin area. Set `USE_DJANGO_JQUERY = False` to disable this behaviour.

`JQUERY_URL`
:   By default, jQuery will be loaded from Google's CDN. If you would prefer to
    use a different version put the full URL here.
