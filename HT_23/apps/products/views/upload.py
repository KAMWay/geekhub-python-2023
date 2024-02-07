import logging
import subprocess
import sys

from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView

from apps.products.forms import ProductForm
from apps.products.models import ScrapyTask

logger = logging.getLogger('django')


class ProductUploadView(FormView):
    template_name = 'products/upload.html'
    form_class = ProductForm

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, 'Not access')
            return redirect('index')

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            form = ProductForm(request.POST)
            if form.is_valid():
                ids_str = form.cleaned_data['ids']
                task = ScrapyTask.objects.create(ids_str=ids_str)
                self.run_subprocess(task.id)
                messages.info(request, 'Products scraping start successfully')
            else:
                messages.error(request, 'Form data unsuccessfully')

        redirect_url = request.GET.get('next')
        if redirect_url:
            return redirect(redirect_url)
        else:
            return redirect('products:upload')

    def run_subprocess(self, task_id: int):
        try:
            sys_execute = sys.executable
            subprocess.Popen([
                sys_execute,
                'manage.py',
                'scrape',
                str(task_id)
            ])
            logger.info(f'scraping subprocess by id:{task_id} run successful')
        except Exception:
            logger.error(f'scraping subprocess by id:{task_id} run unsuccessful')
