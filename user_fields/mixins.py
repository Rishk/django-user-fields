from django.conf import settings

import json


def is_json(storage_field):
    try:
        _ = json.loads(storage_field)
        return True
    except:
        return False


class UserFieldMixin:
    """ Mixin that adds the necessary data retrieval and storage
    functions to an object storing data from extra fields. """

    FIELD_STRING = getattr(settings,'USER_FIELDS_ATTR_NAME', 'extra_data')

    def retrieve_extra_data(self, extra_field, formatted=False):
        """ Function that returns the data stored for a given field. """

        storage_field = getattr(self, self.FIELD_STRING)

        if not is_json(storage_field):
            return None

        extra_data = json.loads(storage_field)

        key = extra_field.name

        if key not in extra_data:
            return None
        
        if formatted and extra_data[key]['type'] == 'choice':
            return extra_data[key]['str']
        else:
            return extra_data[key]['data']

    def save_extra_data(self, extra_field, value):
        """ Function that saves the data supplied for a given field to the object. """

        key = extra_field.name
        extra_data = {}
        storage_field = getattr(self, self.FIELD_STRING)

        if is_json(storage_field):

            extra_data = json.loads(storage_field)

        extra_data[key] = {}

        if extra_field.field_type == 'choice':

            extra_data[key]['str'] = dict(extra_field.get_choices_tuple())[value]

        extra_data[key]['data'] = value

        extra_data[key]['type'] = extra_field.field_type

        setattr(self, self.FIELD_STRING, json.dumps(extra_data))

        self.save()

    def save_extra_form_data(self, form):
        """ Function that saves all of the extra field data in a form to the object. """

        for extra_field in form.extra_fields:
            self.save_extra_data(extra_field, form.cleaned_data[extra_field.name])

    def delete_extra_data(self, extra_field):
        """ Function that deletes all of the data associated with a given field. """

        key = extra_field.name
        storage_field = getattr(self, self.FIELD_STRING)

        if is_json(storage_field):
            extra_data = json.loads(storage_field)
            if key in extra_data:
                del extra_data[key]
                setattr(self, self.FIELD_STRING, json.dumps(extra_data))
                self.save()
