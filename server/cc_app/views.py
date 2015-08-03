from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
# Create your views here.
from .forms import UploadFileForm
from .models import Expense
import encryption
from django.conf import settings
import os

@csrf_protect
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST)
        if form.is_valid():
            expense = Expense()
            expense.description = form.cleaned_data['description']
            infile = request.FILES['file']
            filename = infile._get_name()
            outfile = settings.TEMP_DIR + filename + u'.enc'
            encryption.encrypt_file(key=settings.ENC_KEY, in_file=infile, out_filename=outfile)
            with open(outfile, 'rb') as file:
                expense.image.put(file, content_type='image/jpeg')
                expense.save()
            os.remove(outfile)
            return HttpResponseRedirect('/detail/' + str(expense.id) + '/')
    else:
        form = UploadFileForm()
        c = {'form': form}
        c.update(csrf(request))
        return render_to_response('upload.html', c)


def detail(request, slug):
    expense = Expense.objects(id=slug).first()
    #image = expense.image.read()

    c = {'id': str(expense.id), 'description': str(expense.description), 'created_date': str(expense.created_date)}
    return render_to_response('detail.html', c)