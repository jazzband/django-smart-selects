from django.db.models import get_model
from django.http import HttpResponse
from django.utils import simplejson

def filterchain(request, app, model, field, value):
    Model = get_model(app, model)
    keywords = {str(field): str(value)}
    results = Model.objects.filter(**keywords)
    result = []
    for item in results:
        result.append({'value':item.pk, 'display':unicode(item)})
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')
