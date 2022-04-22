function testAnim(x) {
    $('.modal .modal-dialog').attr('class', 'modal-dialog  ' + x + '  animated');
};
var modal_animate_custom = {
    init: function () {
        $('#myModal').on('show.bs.modal', function (e) {
            var anim = "swing";
            testAnim(anim);
        });
        $('#myModal').on('hide.bs.modal', function (e) {
            var anim = "flipOutX";
            testAnim(anim);
        });
        $("a").tooltip();
    }
};
(function ($) {
    modal_animate_custom.init();
})(jQuery);