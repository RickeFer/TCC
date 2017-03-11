from app.models import *


def run_documentos():
    documentos = Documento.objects.all()

    return {'documentos': documentos}