$(document).ready(function(){
    $('.search-text').on('click', function(){
        $(this).closest('form').submit();
    });

    document.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.altKey) {
            $('.search').focus().select();
        }
    });
})
