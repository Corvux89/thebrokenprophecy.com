$('#subraceCollapse').on('click', function () {
    if ($(this).data("closedAll")) {
        $(".subrace-collapse").collapse("show");
    }
    else {
        $(".subrace-collapse").collapse("hide");
    }
    $(this).data("closedAll", !$(this).data("closedAll"));
});
$('#subclassCollapse').on('click', function () {
    if ($(this).data("closedAll")) {
        $(".subclass-collapse").collapse("show");
    }
    else {
        $(".subclass-collapse").collapse("hide");
    }
    // save last state
    $(this).data("closedAll", !$(this).data("closedAll"));
});
export {};
