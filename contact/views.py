from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail  
from django.template.loader import render_to_string


# Create your views here.

        
def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            email = form.cleaned_data["email"]
            html = render_to_string('email.html', {"subject":subject, "message": message, "email": email})
            
            send_mail("Contact form Subject", "Contact Form Message",["mail@mail.com"], ["kansal.samridhi@gmail.com"], html_message= html)
            messages.success(request,"The email is sent sucessfully")
            return render (request, "contact.html", {"message":message})
        else:
            messages.error(request, "There is some error")
    return render(request, "contact.html", {"form": form})