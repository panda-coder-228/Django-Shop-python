class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        # using for fields
        for field_name, field in self.fields.items():
            
            # add bootstrap CSS class
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} form-control".strip()

            field.widget.attrs["autocomplete"] = "off"

            # set the placeholder from the field lable
            field.widget.attrs.setdefault(
                "placeholder", field.label
            )
            # attrebute required for the fields
            if field.required:
                field.widget.attrs["required"] = True

            