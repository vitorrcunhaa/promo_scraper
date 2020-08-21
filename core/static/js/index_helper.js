 $(function () {
    $("#sidebarToggle").click(function (e) {
        e.preventDefault();
        $("body").toggleClass("sidebar-toggled");
        $(".sidebar").toggleClass("toggled");
    });
    $("span#value-to-dollar").each(function() {
        var dollars = parseFloat(this.textContent)/100;
        $(this).text(dollars.toLocaleString("en-US", {style:"currency", currency:"USD"}));
    });
});