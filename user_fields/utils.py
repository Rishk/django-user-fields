from django.utils.text import slugify
import uuid


def generate_field_name(field_class, field_label, max_tries=10000, use_uuid=True):
    """Function that takes the label of a field and tries to generate a unique name for it.
    The 'max_tries' parameter denotes the maximum number of times the function will try to find unique name."""

    def field_name_in_use(_field_class, _name):
        return _field_class.objects.filter(name=_name).count() > 0

    field_name = slugify(field_label)

    if not field_name_in_use(field_class, field_name):
        return field_name

    for i in range(1, max_tries + 1):
        if not field_name_in_use(field_class, field_name + str(i)):
            return field_name + str(i)

    if use_uuid:
        field_name = str(uuid.uuid4())
        while field_name_in_use(field_class, field_name):
            field_name = str(uuid.uuid4())

        return field_name

    return None
