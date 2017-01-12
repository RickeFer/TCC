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