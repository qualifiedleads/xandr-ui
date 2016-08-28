import  datetime
from ..report import nexus_get_objects_by_id
from django.db import models
from pytz import utc

def load_foreign_objects(cls, field_name, ObjectClass, from_date, to_date):
    try:
        print 'Try to save {}, needed for field {} in class {}'.format(ObjectClass, field_name, cls.__name__)
        filter_params = { field_name+'__name':None}
        try:
            cls._meta.get_field('hour')
            filter_params['hour__gte']=from_date
            filter_params['hour__lte']=to_date
        except:
            filter_params['day__gte']=from_date
            filter_params['day__lte']=to_date

        # .exclude(**{ field_name+'_id':None})\
        ids_missing = cls.objects.filter(**filter_params)\
            .values_list(field_name+'_id', flat=True).distinct()
        ids_missing = set(ids_missing) - set([None, 0])
        saved_ids = nexus_get_objects_by_id(None, ObjectClass, ids_missing)
        if saved_ids != ids_missing:
            print 'Some {}s not saved'.format(field_name)
        return saved_ids
    except Exception as e:
        print 'Error by saving foreign objects for field {}. {}'.format(field_name, e.message)

class PostLoadMix(object):
    @classmethod
    def post_load(self, day):
        from_date = datetime.datetime(day.year, day.month, day.day, tzinfo=utc)
        to_date = from_date
        if hasattr(self,'hour'):
            to_date += datetime.timedelta(hours=23)
        foreign_keys = [field  for field in self._meta.fields
                        if isinstance(field, models.ForeignObject)]
        for f in foreign_keys:
            load_foreign_objects(self, f.name, f.related_model, from_date, to_date)

