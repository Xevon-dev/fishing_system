from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.utils import timezone
import re

from catalog.models import FishSpecies
from .models import Catches, FishingTrips


class CatchForm(forms.ModelForm):
    fish_name = forms.CharField(
        label="Вид риби",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "placeholder": "Введи назву або обери зі списку",
            "role": "combobox",
            "aria-autocomplete": "list",
            "aria-expanded": "false",
        }),
    )
    custom_tackle = forms.CharField(
        label="Оснастка",
        required=False,
        max_length=200,
        widget=forms.TextInput(),
    )
    caught_at = forms.DateTimeField(
        label="Дата й час улову", required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Catches
        fields = (
            "fish_name", "custom_tackle", "weight_kg", "quantity",
            "caught_at", "bait_note",
        )
        labels = {
            "weight_kg": "Вага, кг",
            "quantity": "Кількість, шт.",
            "bait_note": "На що зловив рибу (необов’язково)",
        }
        widgets = {
            "weight_kg": forms.NumberInput(attrs={"min": "0.01", "step": "0.01", "max": "500"}),
            "quantity": forms.NumberInput(attrs={"min": "1", "step": "1", "max": "10000"}),
            "bait_note": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity"].required = False
        if self.instance.pk:
            self.initial["fish_name"] = (
                self.instance.custom_fish_name
                or (self.instance.fish.name if self.instance.fish_id else "")
            )
            self.initial["custom_tackle"] = (
                self.instance.tackle_note
                or (self.instance.tackle.name if self.instance.tackle_id else "")
            )
        # Historical catches did not have timestamps; don't invent one.
        if self.instance.pk and self.instance.caught_at is None:
            self.fields["caught_at"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        fish_name = self.cleaned_data.get("fish_name", "").strip()
        matched_fish = FishSpecies.objects.filter(name__iexact=fish_name).first() if fish_name else None
        instance.fish = matched_fish
        instance.custom_fish_name = "" if matched_fish else fish_name
        custom_tackle = self.cleaned_data.get("custom_tackle", "").strip()
        instance.tackle = None
        instance.tackle_note = custom_tackle
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    def clean_weight_kg(self):
        weight = self.cleaned_data["weight_kg"]
        if weight is not None and weight <= 0:
            raise forms.ValidationError("Вага має бути більшою за нуль.")
        if weight is not None and weight > 500:
            raise forms.ValidationError("Вага однієї риби не може перевищувати 500 кг.")
        return weight

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity is not None and quantity < 1:
            raise forms.ValidationError("Вкажи ціле число від 1.")
        if quantity is not None and quantity > 10000:
            raise forms.ValidationError("Максимум 10 000 риб в одному записі.")
        return quantity

    def clean_fish_name(self):
        name = self.cleaned_data["fish_name"].strip()
        if name and (not any(char.isalpha() for char in name) or re.search(r"[^\w\s'’().-]", name)):
            raise forms.ValidationError("Вкажи коректну назву риби.")
        return name

    def clean_custom_tackle(self):
        tackle = self.cleaned_data["custom_tackle"].strip()
        if tackle and not any(char.isalpha() for char in tackle):
            raise forms.ValidationError("Вкажи назву оснастки текстом.")
        return tackle

    def clean_bait_note(self):
        bait = self.cleaned_data["bait_note"].strip()
        if len(bait) > 500:
            raise forms.ValidationError("Максимум 500 символів.")
        return bait

    def clean_caught_at(self):
        caught_at = self.cleaned_data["caught_at"]
        if caught_at and caught_at > timezone.now():
            raise forms.ValidationError("Не можна вказати час улову з майбутнього.")
        return caught_at


class CatchFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            data = getattr(form, "cleaned_data", {})
            if data.get("DELETE"):
                continue
            populated = any(data.get(field) for field in (
                "fish_name", "custom_tackle", "weight_kg", "quantity",
                "caught_at", "bait_note",
            ))
            if not populated:
                continue
            if not data.get("fish_name", "").strip():
                form.add_error("fish_name", "Вкажи або обери вид риби.")
            if not data.get("quantity"):
                form.add_error("quantity", "Вкажи кількість риби.")
            is_legacy_without_time = form.instance.pk and form.instance.caught_at is None
            if not data.get("caught_at") and not is_legacy_without_time:
                form.add_error("caught_at", "Вкажи дату й час улову.")
CatchInlineFormSet = inlineformset_factory(
    FishingTrips, Catches, form=CatchForm, formset=CatchFormSet,
    extra=1, can_delete=True, max_num=100, validate_max=True, absolute_max=100,
)
