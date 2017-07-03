function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$( "#complete_placement" ).click(function() {
    hex.tiles_changed.forEach(function(tile){
        console.log(tile, JSON.stringify(tile));
        $.ajax({
            url: '/map/tile_detail/' + tile.id + '/',
            async: false,
            type: "PUT",
            dataType: 'json',
            data: JSON.stringify(tile),
            success: function (response) {

            }
        });
    });
    hex.game_info.turn_phase = 'attack';
    hex.update_game_info();
    hex.increment_turn_phase();
    location.reload();
});

$( "#undo_all" ).click(function() {
    if (hex.actions.length > 0){
        hex.actions.forEach(function(action){
            action.tile.units--;
        });
        hex.tiles_changed = [];
        hex.actions = [];
        hex.draw();
    }
});

$( "#undo_last" ).click(function() {
    if (hex.actions.length > 0){
        var last_action = hex.actions.slice(-1)[0];
        last_action.tile.units = last_action.tile.units - last_action.amount;
        hex.actions.pop();
        hex.draw();
    }
});