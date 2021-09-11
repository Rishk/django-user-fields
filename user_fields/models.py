from django.db import models
from django.core.validators import RegexValidator, MinValueValidator


extra_field_types = (
    ('char', 'Text Field'),
    ('text', 'Large Text Field'),
    ('boolean', 'Boolean Field (True/False)'),
    ('choice', 'Choice Field (Drop-down)'),
    ('email', 'Email Field'),
)


class ExtraField(models.Model):
    """ Base model of an extra field that can be created by users.
    It is recommended that you extend this model to add some more fields to allow for easy filtering of fields. """

    slug_regex = RegexValidator(regex=r'^[a-z0-9]+(?:-[a-z0-9]+)*$',
                                message='This identifier can only be made up of lowercase letters, numbers and '
                                        'hyphens.')

    name = models.CharField(validators=[slug_regex], max_length=50, unique=True,
                            help_text='Unique identifier for this field. Formatted like a slug.')

    label = models.CharField(max_length=100)

    help_text = models.TextField(blank=True, null=True, help_text='Optional.')

    required = models.BooleanField()

    field_type = models.CharField(choices=extra_field_types, max_length=8)

    max_length = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)],
                                                  blank=True,
                                                  null=True,
                                                  help_text='For the normal text field only. You can specify the '
                                                            'maximum number of characters for the field.')

    choices = models.CharField(max_length=200,
                               blank=True,
                               null=True,
                               help_text='For the choice field only. Options should be separated by commas. For '
                                         'example: Option 1,Option 2,Option 3')

    def get_choices_tuple(self):

        choices_list = [('', '---------')]

        for i, choice in enumerate(self.choices.split(',')):

            choices_list.append((str(i), choice))

        return tuple(choices_list)

    def __str__(self):

        return '{} ({})'.format(self.label, self.name)


class UserDataField(models.CharField):
    """ Field for storing data from extra fields. """

    def __init__(self, *args, **kwargs):

        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['max_length'] = kwargs.pop('max_length', 30000)

        super(models.CharField, self).__init__(*args, **kwargs)
