/*
 * funcao que retorna array de caracteres com acento
 */
function getArrayCharEspecial(){
    return [
        'á', 'à', 'â', 'ã', 'ä',
        'é', 'è', 'ê', 'ë',
        'í', 'ì', 'î', 'ï',
        'ó', 'ò', 'ô', 'õ', 'ö',
        'ú', 'ù', 'û', 'ü',
        'ç', '!', '?', '*', '&',
        '%', '$', '#', '@', '+',
        '=', '/', ',', '.',
        ';', ':', '´', '`', '~',
        '^', '¨', 'ª', 'º', ' ',
        '[', ']', '>', '<'
    ];
}

/*
 * funcao para substituir espacos por underscore
 * e retirar caracteres especiais
 */
function normalizarNome(nome){
    var arrayEsp = getArrayCharEspecial();

    var flag = false;
    for(var i=0; i<nome.length; i++)
        for(var j=0; j<arrayEsp.length; j++)
            if(nome[i].toLowerCase() == arrayEsp[j]){
                flag = true;
                break;
            }

    if(flag){
        nome = nome.replace(/[ÀÁÂÃÄÅ]/, 'A').replace(/[àáâãäå]/, 'a');
        nome = nome.replace(/[ÈÉÊË]/, 'E').replace(/[èéêë]/, 'e');
        nome = nome.replace(/[ìíîï]/, 'i').replace(/[ÌÍÎÏ]/, 'I');
        nome = nome.replace(/[òóôõö]/, 'o').replace(/[ÒÓÔÕÖ]/, 'O');
        nome = nome.replace(/[ùúûü]/, 'u').replace(/[ÙÚÛÜ]/, 'U');
        nome = nome.replace(/[Ç]/, 'C').replace(/[ç]/, 'c');
        nome = nome.replace(' ', '_');
        nome = nome.replace(/[!?*&%$#@+=/´`^~¨,.:;ªº<>]/, '');

        return normalizarNome(nome);
    }
    else
        return nome;
}

/*
 * INICIO
 * FUNCOES USADAS PARA SETAR DEPENDENCIA
 */
function mostrarOp(campo){
    var id = "#"+campo+"_op";
    $(id).fadeIn(500);
}

function esconderOp(campo){
    var id = "#"+campo+"_op";
    $(id).hide();
}

function setarDependencia(campo, dependencia){
    var cont = 0;
    var classe = campo+'_dependencia';
    $("."+classe).each(function(){
        cont++;
    });

    if(dependencia){
        var aux = dependencia.split(' ')
        var tam = aux.length;

        for(var i=0; i<tam; i++){
            if(aux[i]){
                var dep = document.createElement('input');
                $(dep).attr({
                    'type': 'hidden',
                    'id': campo+'_dependencia_'+cont,
                    'name': campo+'_dependencia_'+cont,
                    'class': campo+'_dependencia',
                    'value': aux[i]
                });

                var id_campo = "#"+campo+"_campo";
                $(id_campo).addClass("dependente");
                $(id_campo).append($(dep));

                $("#li_chave_"+campo).hide();
                $("#"+campo+"_"+dependencia).hide();

                cont++;
            }
        }
    }
}

function limparDependencia(campo){
    var classe = "."+campo+'_dependencia';
    var id_campo = "#"+campo+"_campo";

    $(classe).remove();
    $(id_campo).removeClass("dependente");

    $("#li_chave_"+campo).show();
    $(".item_chave_"+campo).show();
}

function getSelect(dados){


    console.log(dados);
}