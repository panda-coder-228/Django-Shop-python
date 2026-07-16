class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        # using for fields
        for field_name, field in self.fields.items():
            #общий класс bootstrap
            field.widget.attrs["class"] = "form-control"

            field.widget.attrs["autocomplete"] = "off"

            # placeholder for label_fiels
            if field.label:
                field.widget.attrs["placeholder"] = field.label

            # attrebute required
            if field.required:
                field.widget.attrs["required"] = True

            