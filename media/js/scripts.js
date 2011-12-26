/**
 * Created by IntelliJ IDEA.
 * User: ZTRELETS
 * Date: 15.11.2010
 * Time: 14:09:22
 * To change this template use File | Settings | File Templates.
 */
function toggleSearchPanel(){
    $("a.toggleSearchPanel").click(function () {
        if ($("#searchPanelForm").is(":hidden")){
            $("#searchPanel").animate({height: "180px"}, 'fast' );
            $("#searchPanel a.toggleSearchPanel").html("скрыть панель поиска").removeClass("close").addClass("open");
            $("#searchPanelForm").fadeIn(200);
        }
        else{
            $("#searchPanel").animate({height: "20px"}, 'fast' );
            $("#searchPanel a.toggleSearchPanel").html("расширенный поиск").removeClass("open").addClass("close");
            $("#searchPanelForm").fadeOut(100);
        }
    });
    return false;
};