from app.models import *


def run_documentos():
    documentos = Document.objects.all()

    return {'documentos': documentos}