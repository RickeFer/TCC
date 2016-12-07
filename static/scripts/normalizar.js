$(function(){
    //$(".sortable").each(function(){
        $("#sortable").sortable({
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
/*
$("#add_tabela").click(function(){
    $.ajax({
        url: 'ajax_add_tabela',
        type: 'POST',
        success: function(json){
            $("body").html(json);
        }
    });
});*/
