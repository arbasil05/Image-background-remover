# views.py
from django.shortcuts import render
from rembg import remove
from PIL import Image
from django.views.decorators.csrf import csrf_protect
import base64
import io
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
import os
from django.conf import settings
from datetime import datetime

def home(request):
    return render(request, 'home.html')

@csrf_protect
def action(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            print("Image uploaded succesfully")
            print(f"Image recieved: {uploaded_file}")
            x = Image.open(uploaded_file)
            print("Removing background")
            result = remove(x)
            print("Successful")

            # Save the image in memory for displaying in Result.html
            image_io = io.BytesIO()
            result.save(image_io, format='PNG')
            image_data = base64.b64encode(image_io.getvalue()).decode('utf-8')

            # Generate a unique filename based on timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f'convert_{timestamp}.png'

            # Store the image data and filename in the session
            request.session['result_image_data'] = image_data
            request.session['result_filename'] = filename

            return render(request, 'Result.html', {'Result': f'data:image/png;base64,{image_data}', 'filename': filename})

    return render(request, 'Home.html')

def download_image(request):
    # Retrieve image data and filename from the session
    image_data = request.session.get('result_image_data')
    filename = request.session.get('result_filename', 'convert.png')  # Default to 'convert.png' if not provided
    print(f"Downloading image : {filename}")
    print("Process completed succesfully")

    if image_data:
        # Clear the session data after retrieving it
        request.session.pop('result_image_data', None)
        request.session.pop('result_filename', None)

        # Return the image data as a downloadable response
        response = HttpResponse(base64.b64decode(image_data), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    else:
        return HttpResponse("Image data not found in session.")
