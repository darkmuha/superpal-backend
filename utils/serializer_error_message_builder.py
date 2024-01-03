class SerializerErrorMessageBuilder:
    def __init__(self):
        self.required_fields = []
        self.invalid_fields = []
        self.already_used_fields = []

    def add_required_field(self, field):
        self.required_fields.append(field)

    def add_invalid_field(self, field):
        self.invalid_fields.append(field)

    def add_already_used_field(self, field):
        self.already_used_fields.append(field)

    def build(self):
        error_message = ""

        if self.required_fields:
            required_fields_message = ", ".join(self.required_fields)
            error_message += f"{required_fields_message} {'are' if len(self.required_fields) > 1 else 'is'} required"

        if self.invalid_fields:
            invalid_fields_message = ", ".join(self.invalid_fields)
            error_message += (
                f"{', and ' if error_message else ''}{invalid_fields_message} "
                f"{'do not have' if len(self.invalid_fields) > 1 else 'does not have'} a valid format"
            )

        if self.already_used_fields:
            already_used_fields_message = ", ".join(self.already_used_fields)
            error_message += (
                f"{', and ' if error_message else ''}{already_used_fields_message} "
                f"{'have' if len(self.already_used_fields) > 1 else 'has'} already been used"
            )

        return error_message.capitalize()
