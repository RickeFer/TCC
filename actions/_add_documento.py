from app.forms import DocumentForm, FieldForm
from app.models import Document


def run_add_documento(request):
    if request.method != 'POST':
        formDoc = DocumentForm()
        formCamp = FieldForm()
    else:
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return None

    return {'formDoc': formDoc, 'formCamp': formCamp}