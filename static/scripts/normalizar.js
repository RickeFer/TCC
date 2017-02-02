$(function(){
    //$(".sortable").each(function(){
        $(".sortable").sortable({
            revert: true,
            //axis: "x"
        });


        $("#teste").sortable({
            revert: true,
            //axis: "x"
        });


    /*$("#draggable").draggable({
        connectToSortable: "#sortable",
        helper: "clone",
        revert: "invalid",
    });*/

    //$("ul, li").disableSelection();
});

function atualizaClasse(){
    $(".sortable").each(function(){
        $(this).sortable({
            revert: true
        });
    });
}

function atualizaPosCampo(id){
    id = "#"+id;

    console.log(id);
}
