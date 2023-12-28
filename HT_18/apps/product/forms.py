from django import forms


class ProductForm(forms.Form):
    ids = forms.CharField(
        min_length=10,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the ids separated by comma',
                # 'aria - describedby': 'formHelpBlock',
            }
        )
    )

    def is_valid(self):
        if not super().is_valid():
            return False

        ids_str = self.cleaned_data['ids']
        ids = [item.strip() for item in ids_str.split(sep=',')]

        return all(self.__is_valid_id(id) for id in ids)

    def __is_valid_id(self, id: str):
        if len(id) == 0:
            return False

        return id[:1].isalpha() and id[1:].isdigit()
