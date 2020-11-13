$(document).ready(function () {

    var baseUrl = 'http://localhost:8000/';
    var deleteBtn = $('.bi-trash');
    var searchBtn = $('#bi-search');
    var searchForm = $('#search-form');
    var filter = $('#filter');

    $(deleteBtn).on('click', function(e) {
        e.preventDefault();

        var delLink = $(this).attr('href');
        var result = confirm('Are you sure you want to delete this task?');

        if(result) {
            window.location.href = delLink;
        }
    });

    $(searchBtn).on('click', function () {
        searchForm.submit()
    });

    $(filter).change(function () {
        var filter = $(this).val();
        console.log(filter);

        window.location.href = baseUrl + '?filter=' + filter;
    })
});
