var searchInput = $('#search_input')
var autocomplete = searchInput.yourlabsAutocomplete({
    url: searchInput.data('url'),
    choiceSelector: 'span',
    hideAfter: 200,
    minimumCharacters: 1,
    placeholder: searchInput.attr('placeholder'),
    appendAutocomplete: $('#search_input')
});
searchInput.bind('selectChoice', function(e, choice, autocomplete) {
    if(choice[0].children[0] == undefined) {
        $('#search_input').val(choice[0].innerHTML);
        $('#search').submit();
    }
});
