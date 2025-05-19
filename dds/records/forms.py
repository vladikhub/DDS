from django import forms
from django.db.models.query_utils import class_or_instance_method
from unicodedata import category

from records.models import Records, Category, Subcategory


class RecordForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'type' in self.data:
            type_id = int(self.data.get('type'))
            self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)

        if 'category' in self.data:
            category_id = int(self.data.get('category'))
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
        elif self.instance.pk:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
