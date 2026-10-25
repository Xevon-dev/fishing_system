from django import forms

from .models import FishingTrips


class GenericFishingTripForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["water_body"].queryset = self.fields["water_body"].queryset.order_by("name")
        self.fields["water_body"].label_from_instance = lambda water: water.name

    class Meta:
        model = FishingTrips
        fields = ("water_body", "type", "method_note", "note")
        labels = {
            "water_body": "Водойма",
            "type": "Тип риболовлі",
            "method_note": "Техніка лову",
            "note": "Нотатка",
        }
        widgets = {
            "note": forms.Textarea(attrs={"rows": 4}),
        }
