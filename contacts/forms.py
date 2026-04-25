from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "address", "email", "phone"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        contacts = Contact.objects.filter(email__iexact=email)

        if self.instance.pk:
            contacts = contacts.exclude(pk=self.instance.pk)

        if contacts.exists():
            raise forms.ValidationError("This email address is already in use.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if not phone.isdigit() or len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError(
                "Enter a valid phone number with 10 to 15 digits."
            )

        contacts = Contact.objects.filter(phone=phone)

        if self.instance.pk:
            contacts = contacts.exclude(pk=self.instance.pk)

        if contacts.exists():
            raise forms.ValidationError("This phone number is already in use.")

        return phone
