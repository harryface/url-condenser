// Jquery Auto Search 

const user_input = $("#id_custom_shortcode") //id of the input field
const container = $("#replaceable-content")   //id of the replaceable container
const endpoint = "/search/"    //Search url endpoint
const delay_by_in_ms = 700  //7 seconds before running
let scheduled_function = false


let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters).done(response => {
        // fade out the container
        container.fadeTo("slow", 0).promise().then(() => {
            // replace the content
            container.html(response["message"]);
            // fade-in the container with new content
            container.fadeTo("slow", 1)
            console.log(request_parameters)
        })
    })
}


user_input.on('keyup', function () {

    const request_parameters = {
        q: $(this).val() // value of user_input
    }

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})