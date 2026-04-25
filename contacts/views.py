from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import Contact


def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "contact_list.html", {"contacts": contacts})


def add_contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("contact_list")

    return render(request, "add_contact.html", {"form": form})


def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    form = ContactForm(request.POST or None, instance=contact)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("contact_list")

    return render(request, "edit_contact.html", {"form": form})


@require_POST
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    return redirect("contact_list")
