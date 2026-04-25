from django.test import TestCase
from django.urls import reverse

from .models import Contact


class ContactViewsTests(TestCase):
    def valid_payload(self, **overrides):
        payload = {
            "first_name": "Alice",
            "last_name": "Smith",
            "address": "221B Baker Street",
            "email": "alice@example.com",
            "phone": "9876543210",
        }
        payload.update(overrides)
        return payload

    def test_contact_list_displays_saved_contacts(self):
        contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            address="Main Street",
            email="john@example.com",
            phone="9876543211",
        )

        response = self.client.get(reverse("contact_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, contact.first_name)
        self.assertContains(response, contact.email)

    def test_add_contact_with_valid_data_creates_contact(self):
        response = self.client.post(reverse("add_contact"), self.valid_payload())

        self.assertRedirects(response, reverse("contact_list"))
        self.assertTrue(Contact.objects.filter(email="alice@example.com").exists())

    def test_add_contact_rejects_blank_required_fields(self):
        response = self.client.post(
            reverse("add_contact"),
            self.valid_payload(
                first_name="",
                last_name="",
                address="",
                email="",
                phone="",
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)
        self.assertContains(response, "This field is required.")

    def test_add_contact_rejects_invalid_email(self):
        response = self.client.post(
            reverse("add_contact"),
            self.valid_payload(email="not-an-email"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)
        self.assertContains(response, "Enter a valid email address.")

    def test_add_contact_rejects_invalid_phone(self):
        response = self.client.post(
            reverse("add_contact"),
            self.valid_payload(phone="123"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)
        self.assertContains(response, "Enter a valid phone number with 10 to 15 digits.")

    def test_add_contact_rejects_duplicate_email(self):
        Contact.objects.create(**self.valid_payload())

        response = self.client.post(
            reverse("add_contact"),
            self.valid_payload(phone="9876543219"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertContains(response, "This email address is already in use.")

    def test_add_contact_rejects_duplicate_phone(self):
        Contact.objects.create(**self.valid_payload())

        response = self.client.post(
            reverse("add_contact"),
            self.valid_payload(email="another@example.com"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertContains(response, "This phone number is already in use.")

    def test_edit_contact_updates_valid_data(self):
        contact = Contact.objects.create(**self.valid_payload())

        response = self.client.post(
            reverse("edit_contact", args=[contact.id]),
            self.valid_payload(
                first_name="Alicia",
                email="alicia@example.com",
                phone="9876543222",
            ),
        )

        contact.refresh_from_db()

        self.assertRedirects(response, reverse("contact_list"))
        self.assertEqual(contact.first_name, "Alicia")
        self.assertEqual(contact.email, "alicia@example.com")
        self.assertEqual(contact.phone, "9876543222")

    def test_edit_contact_rejects_duplicate_email(self):
        Contact.objects.create(**self.valid_payload())
        contact = Contact.objects.create(
            **self.valid_payload(
                first_name="Bob",
                email="bob@example.com",
                phone="9876543233",
            )
        )

        response = self.client.post(
            reverse("edit_contact", args=[contact.id]),
            self.valid_payload(
                first_name="Bob",
                email="alice@example.com",
                phone="9876543233",
            ),
        )

        contact.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(contact.email, "bob@example.com")
        self.assertContains(response, "This email address is already in use.")

    def test_delete_requires_post(self):
        contact = Contact.objects.create(**self.valid_payload())

        response = self.client.get(reverse("delete_contact", args=[contact.id]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Contact.objects.filter(id=contact.id).exists())

    def test_delete_contact_removes_record(self):
        contact = Contact.objects.create(**self.valid_payload())

        response = self.client.post(reverse("delete_contact", args=[contact.id]))

        self.assertRedirects(response, reverse("contact_list"))
        self.assertFalse(Contact.objects.filter(id=contact.id).exists())
