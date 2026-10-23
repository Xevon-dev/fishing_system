from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from catalog.models import FishSpecies
from .models import Catches, FishingTrips


class CatchForm(forms.ModelForm):
    caught_at = forms.DateTimeField(
        label="Дата й час улову", required=True,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Catches
        fields = ("fish", "weight_kg", "quantity", "caught_at")
        labels = {"fish": "Риба", "weight_kg": "Вага улову, кг", "quantity": "Кількість, шт."}
        widgets = {
            "weight_kg": forms.NumberInput(attrs={"min": "0.01", "step": "0.01", "max": "999999.99"}),
            "quantity": forms.NumberInput(attrs={"min": "1", "step": "1"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fish"].queryset = FishSpecies.objects.order_by("name")
        self.fields["quantity"].required = True
        # Historical catches did not have timestamps; don't invent one.
        if self.instance.pk and self.instance.caught_at is None:
            self.fields["caught_at"].required = False

    def clean_weight_kg(self):
        weight = self.cleaned_data["weight_kg"]
        if weight is not None and weight <= 0:
            raise forms.ValidationError("Вага має бути більшою за нуль.")
        return weight

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity is not None and quantity < 1:
            raise forms.ValidationError("Вкажи ціле число від 1.")
        return quantity


class CatchFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            data = getattr(form, "cleaned_data", {})
            if data.get("DELETE"):
                continue
CatchInlineFormSet = inlineformset_factory(
    FishingTrips, Catches, form=CatchForm, formset=CatchFormSet,
    extra=1, can_delete=True, max_num=100, validate_max=True, absolute_max=100,
)
