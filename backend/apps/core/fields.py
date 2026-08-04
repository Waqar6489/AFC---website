"""Custom serializer fields shared across apps."""

from rest_framework import serializers


class ModelDefaultBooleanField(serializers.BooleanField):
    """A BooleanField that respects the underlying model field's default
    even when submitted via multipart/form-data.

    DRF's stock BooleanField treats a missing key in an HTML form
    submission as `False` (mimicking an unchecked HTML checkbox) rather
    than falling back to the serializer/model default. That's the right
    behaviour for an actual HTML checkbox, but it's a footgun for JSON-ish
    APIs that happen to use multipart only because a sibling field is a
    file upload (e.g. `TeamMember.image`, `Category.image`) — omitting
    `is_active` should mean "use the default", not "force it to False".
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Disabling the HTML-checkbox special case makes the field fall
        # through to normal default resolution instead.
        self.default_empty_html = serializers.empty
