from django import forms


class ProductForm(forms.Form):
    ids = forms.CharField(
        min_length=10,
        max_length=120,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the ids separated by comma',
            }
        )
    )

    def is_valid(self):
        if not super().is_valid():
            return False

        ids_str = self.cleaned_data['ids']
        ids = [item.strip() for item in ids_str.split(sep=',')]

        if len(ids) > 10:
            return False

        return all(self.__is_valid_id(_id) for _id in ids)

    def __is_valid_id(self, _id: str):
        if len(_id) == 0:
            return False

        return all(i.isdigit() or i.isalpha() for i in _id)
