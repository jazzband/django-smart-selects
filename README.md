Django Smart Selects
====================

If you the following model:

	class Location(models.Model)
		continent = models.ForeignKey(Continent)
		country = models.ForeignKey(Country)
		area = models.ForeignKey(Area)
		city = models.CharField(max_length=50)
		street = models.CharField(max_length=100)
		
And you want that if you select a continent only the countries are available that are located on this continent and the same for areas
you can do the following:

class Location(models.Model)
	continent = models.ForeignKey(Continent)
	country = ChainedForeignKey(Country, chained_field="continent", chained_model_field="continent")
	area = ChainedForeignKey(Area, chained_field="country", chained_model_field="country")
	city = models.CharField(max_length=50)
	street = models.CharField(max_length=100)
	
This example asumes that the Country Model has a "continent" field and that the Area model has "country" field.

The chained field is the field on the same model the field should be chained too.
The chained model field is the field of the chained model that corresponds to the model linked too by the chained field.