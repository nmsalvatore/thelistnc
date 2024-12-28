import os, subprocess, zipfile
from io import BytesIO
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, FileResponse
from config import settings

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard/dashboard.html')
    else:
        return redirect('login')

def generate_post(request):
    if request.method == "POST":
        subprocess.run([
            settings.POST_GENERATOR_PYTHON,
            settings.POST_GENERATOR_SCRIPT
        ])

        date_str = datetime.now().strftime("%Y%m%d")
        images_dir = os.path.join(settings.IG_POST_DIR, date_str)

        if not os.path.exists(images_dir):
            return HttpResponseNotFound("No images found for today")

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for filename in os.listdir(images_dir):
                file_path = os.path.join(images_dir, filename)
                if os.path.isfile(file_path):
                    archive_path = os.path.join(f"{date_str}", filename)
                    zip_file.write(file_path, archive_path)

        if zip_buffer.tell() == 0:
            return HttpResponseNotFound("No images found for today")

    zip_buffer.seek(0)
    response = FileResponse(zip_buffer, as_attachment=True, filename=f"thelistnc_ig_post--{date_str}.zip")
    return response
