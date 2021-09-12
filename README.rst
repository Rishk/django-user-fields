django-user-fields
==================

.. image:: https://pepy.tech/badge/django-user-fields
	:target: https://pepy.tech/project/django-user-fields
	:alt: Total downloads

.. image:: https://badge.fury.io/py/django-user-fields.svg
	:target: https://pypi.org/project/django-user-fields/
	:alt: PyPI version

.. image:: https://github.com/Rishk/django-user-fields/actions/workflows/python-publish.yml/badge.svg
	:target: https://github.com/Rishk/django-user-fields/actions/workflows/python-publish.yml
	:alt: GitHub release publish action

A Django application that makes user creation of form fields simple, handling everything from form generation to data storage and retrieval.

This was initially built for `MUN Manager <https://modelun.co>`_ to allow conferences to collect whatever information they wanted to during all parts of the registration process. django-user-fields allows conferences to easily add their own extra fields to various forms using a simple admin interface creating a tailored experience.

Simple Installation and Usage Guide
===================================

1. Install ``django-user-fields``:

.. code-block::

    $ pip install django-user-fields

2. Add ``user_fields`` to your installed apps:

.. code-block::

    INSTALLED_APPS = (
        ...
        'user_fields',
        ...
    )

3. Run a database migration:

.. code-block::

    $ python manage.py migrate

4. Create an ``ExtendedExtraField`` model:

.. code-block::

    from user_fields.models import ExtraField

    class ExtendedExtraField(ExtraField):

        # You can add any custom fields you'd like here to make filtering fields easier.
        # A list of all predefined fields can be found below.

5. Add the ``@initialise_extra_fields`` decorator to your form:

.. code-block::

    from user_fields.decorators import initialise_extra_fields

    @initialise_extra_fields
    class ExampleForm(forms.ModelForm):

6. Add the ``UserFieldMixin`` to the object(s) you would like to have extra fields:

.. code-block::

    from user_fields.mixins import UserFieldMixin

    class ExampleObject(models.Model, UserFieldMixin):

7. Add a ``UserDataField`` to the object for storage and migrate:

.. code-block::

    from user_fields.models import UserDataField, ExtraField

    class ExampleObject(models.Model, UserFieldMixin):

        extra_data = UserDataField()

    $ python manage.py migrate

**Note**: If ``extra_data`` is taken and/or you would like to name the storage field something else, you can define ``USER_FIELDS_ATTR_NAME`` in your settings.

8. Create and pass some extra fields to your form:

.. code-block::

    extra_fields = ExtendedExtraField.objects.filter(parameter=something)

    form = ExampleForm(... extra_fields=extra_fields, ...)

9. Add an extra line to save the extra fields to your object:

.. code-block::

    object = form.save()
    object.save_extra_form_data(form) # Ensures that both object and form save functions are not overwritten.

Supported Fields
================

- ``CharField``
- ``CharField With Choices``
- ``TextField``
- ``BooleanField``
- ``EmailField``

Feel free to submit a pull request if you would like to add more fields. Most fields should be relatively easy to add, although ``FileField`` will be an interesting challenge!

``ExtraField`` Attributes
=========================

+-------------+------------+---------------------------------------------------+------------------------------+
| Proper Name | Name       | Description                                       | Example                      |
+=============+============+===================================================+==============================+
| Name        | name       | Equivalent to the HTML ``input`` name parameter.  | example-field (slug format)  |
+-------------+------------+---------------------------------------------------+------------------------------+
| Label       | label      | Django form field label (rendered name).          | Example Field                |
+-------------+------------+---------------------------------------------------+------------------------------+
| Help Text   | help_text  | Django form field help text.                      | This is some guidance.       |
+-------------+------------+---------------------------------------------------+------------------------------+
| Required    | required   | Django form field required parameter.             | True / False                 |
+-------------+------------+---------------------------------------------------+------------------------------+
| Field Type  | field_type | Dropdown with all supported fields.               | CharField (char)             |
+-------------+------------+---------------------------------------------------+------------------------------+
| Max. Length | max_length | CharField (only) max length.                      | 35                           |
+-------------+------------+---------------------------------------------------+------------------------------+
| Choices     | choices    | Choices for the ``CharField With Choices``.       | Option 1,Option 2,Option 3   |
+-------------+------------+---------------------------------------------------+------------------------------+

``UserFieldMixin`` Functions
============================

``.retrieve_extra_data(ExtraField, formatted=True/False)``: Returns the data stored for a given field. If formatted is True, it will return the `value` for the ``CharField With Choices``, otherwise it will return the `key` of the choice.

``.save_extra_data(ExtraField, data)``: Saves the data supplied for a given field to the object.

``.save_extra_form_data(Form)``: Saves all of the extra field data in a form to the object.

``.delete_extra_data(ExtraField)``: Deletes all of the data associated with a given field.

To Do
=====

- Improve documentation.
- Implement testing.
- Add support for more fields.
