/**
 * Created by marta on 25.04.17.
 */


window.onload = function () {
    $('#addBt').hide('fast');
    $('#updateBt').hide();
    $('#deleteBt').hide();

    $('#id_date').attr('readonly','readonly');

    $("td").click(function (event) {
        var date = event.target.closest('td').id;
        if (date) {
            getWorkoutByDate(date);
            $('input[name=date]').val(date);
        }
        else {
            $('#addBt').hide();
            $('#updateBt').hide();
            $('#deleteBt').hide();
        }
    });
};

function getWorkoutByDate(date) {
    var today = new Date();
    var received_date = new Date(date);
    if (today < received_date) {
        // console.log("today is before clicked date!");
         $('#id_done').attr("disabled", true);
    } else {
        $('#id_done').removeAttr("disabled");
    }
    $.ajax({
        url: '/calendar/display_form',
        method: 'GET',
        data: {
            date: date
        },
        success: function () {
            response_args = arguments[0];
            if (response_args.length > 2) {
                // updating
                console.log("Updating");
                $('#addBt').hide();
                $('#updateBt').show();
                $('#deleteBt').show();
                response_args = JSON.parse(response_args);
                console.log(response_args);
                console.log(response_args.title);
                if(response_args.done === true) {
                    $('#id_done').prop("checked", true);
                }
                else {
                    $('#id_done').prop("checked", false);
                }
                $('textarea').val(response_args.comment);
                $('input[name=runner]').val(response_args.runner);
                $('input[name=title]').val(response_args.title);
                $('input[name=distance]').val(response_args.distance);
            }
            else {
                // creating new
                console.log("Creating new");
                $('textarea').val("");
                $('input[name=runner]').val("");
                $('input[name=distance]').val("");
                $('input[name=title]').val("");
                $('#id_done').prop("checked", false);
                $('#addBt').show();
                $('#updateBt').hide();
                $('#deleteBt').hide();
            }
        }
    });
}

function sendFormRequest(type) {
    var request_url = '/calendar/' + type + '/';
    $.ajax({
        url: request_url,
        type: "POST",
        data: $('#workoutForm').serialize(),
        success: function () {
            console.log("sendFormRequest");
            window.location.reload();
            response_args = arguments[0];
        }
    });
}

function changeMonth(type) {
    var request_url = '/calendar/change_month';
    var date = $( ".day" ).first().attr('id');
    $.ajax({
        url: request_url,
        type: "GET",
        data: {
            'date' : date,
            'type' : type
        },
        success: function () {
            response_args = JSON.parse(arguments[0]);
            origin = window.location.origin;
            $(location).attr('href', origin + '/calendar/' + response_args.year + '/' +
            response_args.month);
        }
    })

}