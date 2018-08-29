from django.utils.text import slugify


def generate_field_name(field_class, field_label, max_tries=10000):
    """ Function that takes the label of a field and tries to generate a unique name for it.
    The 'max_tries' parameter denotes the maximum number of times the function will try to find unique name. """

    def field_name_in_use(_field_class, _name):

        if _field_class.objects.filter(name=_name).count() == 0:

            return False

        else:

            return True

    field_name = slugify(field_label)

    if field_name_in_use(field_class, field_name):

        for i in range(1, max_tries+1):

            if field_name_in_use(field_class, field_name+str(i)) is False:

                return field_name + str(i)
                break

        return None

    else:

        return field_name
