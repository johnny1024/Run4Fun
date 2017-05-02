/**
 * Created by marta on 25.04.17.
 */

window.onload = function() {
    $('#addBt').hide('fast');
    $('#updateBt').hide();
    $('#deleteBt').hide();

    $("td").click(function(event) {
        var date = event.target.closest('td').id;
        if(date){
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
    $.ajax({
        url: '/calendar/display_form',
        method: 'GET',
        data: {
            date : date
        },
        success : function () {
            response_args = arguments[0];

            if(response_args.length > 2){
                // updating
                console.log("Updating");
                $('#addBt').hide();
                $('#updateBt').show();
                $('#deleteBt').show();
                response_args = JSON.parse(response_args);
                console.log(response_args.comment);
                $('textarea').val(response_args.comment);
                $('input[name=runner]').val(response_args.runner);
                $('input[name=distance]').val(response_args.distance);
            }
            else {
                // creating new
                console.log("Creating new");
                $('textarea').val("");
                $('input[name=runner]').val("");
                $('input[name=distance]').val("");
                $('#addBt').show();
                $('#updateBt').hide();
                $('#deleteBt').hide();
            }
        }
    });
}

function updateRecord() {
     $.ajax({
        url: '/calendar/update_workout',
        method: 'POST',
        data: {
            'content': $('#workoutForm').serialize(),
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success : function () {
            response_args = arguments[0];
        }
    });
}

function addRecord() {
     $.ajax({
        url: '/calendar/add_workout',
        method: 'POST',
        data: $('#workoutForm').serialize(),
        success : function () {
            response_args = arguments[0];
        }
    });
}

function deleteRecord() {
    $.ajax({
        url: '/calendar/delete_workout',
        method: 'POST',
        data: $('#workoutForm').serialize(),
        success : function () {
            response_args = arguments[0];
        }
    });
}