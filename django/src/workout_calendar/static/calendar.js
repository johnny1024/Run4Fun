/**
 * Created by marta on 25.04.17.
 */

window.onload = function() {

    $("td").click(function(event) {
        alert(event.target.id);
    });
};

