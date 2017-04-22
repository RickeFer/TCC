from classes.util_documento import *
from classes.util_tabela import *

def run_script_documento(request, documento_id):
    documento = get_documento_completo(documento_id)

    script_create, script_alter_primaria, script_alter_estrangeira = '', '', ''

    for tabela in documento.tabelas:
        script_create += gerar_script_create(tabela)
        script_alter_primaria += gerar_script_alter_primaria(tabela)
        script_alter_estrangeira += gerar_script_alter_estrangeira(tabela)

    return {
        'documento': documento, 'script_create': script_create,
        'script_alter_primaria': script_alter_primaria, 'script_alter_estrangeira': script_alter_estrangeira
    }