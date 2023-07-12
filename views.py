from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import invoice
from django.http import HttpResponse
from reportlab.pdfgen import canvas

# Create your views here.
def home(request):
    return render(request, 'core/index.html') 


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")   # Redirect to home page if login is successful
        else:
            error_message = 'Invalid username or password'  # Error message to display if login fails
            return render(request, 'core/login.html', {'error_message': error_message})
    else:
        return render(request, 'core/login.html')  
    
@login_required  
def profile(request):
    data = invoice.objects.filter(Sender=request.user)
    context = {
        'data': data , 
    }
    
    return render(request , "core/profile.html" , context)

def generate_pdf(request , invoice_id):
    # Get the invoice object
    invoices = invoice.objects.get(id=invoice_id)

    # Create a new PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{invoices.Reciever}.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Write the text to the PDF
    p.drawString(100, 100, f"Sender: {invoices.Sender.username}")
    p.drawString(100, 120, f"Receiver: {invoices.Reciever}")
    p.drawString(100, 140, f"Date of shipment: {invoices.Date_shippment}")
    p.drawString(100, 160, f"Price of shipping: {invoices.price_of_shipping}LE")
    p.drawString(100, 180, f"Price of product: {invoices.price_of_product}LE")
    p.drawString(100, 200, f"City: {invoices.city}")
    p.drawString(100, 220, f"Address: {invoices.address}")
    if invoices.order_status:
        status = "Arrived"
    else:
        status = "Not arrived yet"
    p.drawString(100, 240, f"Order status: {status}")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


def logout_view(request):
    logout(request)
    return render(request , "core/index.html")
    
    