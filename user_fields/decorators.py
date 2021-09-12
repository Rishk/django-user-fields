from django import forms


def initialise_extra_fields(django_form):
    """Decorator that initialises the extra fields passed to a given form."""

    def extra_field_init(self, *args, **kwargs):

        if "extra_fields" in kwargs:

            self.extra_fields = kwargs.pop("extra_fields")

            super(django_form, self).__init__(*args, **kwargs)

            for extra_field in self.extra_fields:

                field_type = extra_field.field_type

                if field_type == "char":

                    self.fields[extra_field.name] = forms.CharField(
                        max_length=extra_field.max_length
                    )

                elif field_type == "text":

                    self.fields[extra_field.name] = forms.CharField(
                        widget=forms.Textarea
                    )

                elif field_type == "boolean":

                    self.fields[extra_field.name] = forms.BooleanField()

                elif field_type == "choice":

                    choices_tuple = extra_field.get_choices_tuple()

                    self.fields[extra_field.name] = forms.ChoiceField(
                        choices=choices_tuple
                    )

                elif field_type == "email":

                    self.fields[extra_field.name] = forms.EmailField()

                self.fields[extra_field.name].label = extra_field.label

                self.fields[extra_field.name].required = extra_field.required

                self.fields[extra_field.name].help_text = extra_field.help_text

                self.fields[
                    extra_field.name
                ].initial = self.instance.retrieve_extra_data(extra_field)

        else:

            raise ValueError(
                "Extra fields could not be found. Please ensure you pass extra fields to the form "
                "using the extra_fields parameter."
            )

    django_form.__init__ = extra_field_init

    return django_form
