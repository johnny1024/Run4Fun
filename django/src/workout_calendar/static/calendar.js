/**
 * Created by marta on 25.04.17.
 */
$('document').ready(function(){
    $('#id_calories').on('input', function() {
    getWeight('calories');
    });
    $('#id_time').on('input', function() {
    getWeight('time');
    });
    $('#id_distance').on('input', function() {
    getWeight('distance');
    });
});

window.onload = function () {
    $('#addBt').hide('fast');
    $('#updateBt').hide();
    $('#deleteBt').hide();
    $('#form-container').height($('#wrapper').height() - 6);

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

                getWeight('distance');
            }
            else {
                // creating new
                console.log("Creating new");
                $('textarea').val("");
                $('input[name=runner]').val("");
                $('input[type=number]').val("");
                $('input[name=title]').val("");
                // $
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

function getWeight(type) {
    console.log("getWeight");
    var request_url = '/calendar/get_weight';
    $.ajax({
        url: request_url,
        type: "GET",
        success: function () {
            response_args = JSON.parse(arguments[0]);
            console.log(response_args.weight);
            calculate(type, response_args.weight);
        }
    })
}

function calculate(type, weight) {
    var calories = 0;
    var distance = 0;
    var time = 0;
    var velocity = 9; // 9 km per hour
    if (type === 'distance') {
        distance = parseInt($('#id_distance').val()); // km
        calories = weight * distance; // kilocalories
        time = distance / velocity; // time in hours
    } else if (type === 'calories') {
        calories = parseInt($('#id_calories').val());
        distance = calories / weight;
        time = distance / velocity;
    } else {
        time = parseInt($('#id_time').val());
        distance = time * velocity;
        calories = weight * distance;
    }
    calories = Math.round(calories);
    distance = Math.round(distance);
    time = (Math.round(time*60));
    console.log(time, calories, distance);
    $('#id_calories').val(calories);
    $('#id_distance').val(distance);
    $('#id_time').val(time);
}