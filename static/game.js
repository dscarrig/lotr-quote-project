const $choiceForm = $("#choice-form");
const $correct_name = $("#correct_name")
const $correct_message = $("#correct")
const $incorrect_message = $("#incorrect")
const $next_button = $("#next_button")
const $submit_button = $("#submit_button")

$choiceForm.on("submit", checkAnswer);

function checkAnswer(evt) {
    evt.preventDefault();
    let choice = $choiceForm.serializeArray()[0]["value"];
    let correct_name = $correct_name.text();
    choice = choice.replace(/[\n\r]/g, '').replace(/\s+/g,"");
    correct_name = correct_name.replace(/[\n\r]/g, '').replace(/\s+/g,"");

    console.log(`Chose ${choice} correct is ${correct_name}`)

    if(choice === correct_name){
        $correct_message.removeClass("invisible");
    }
    else{
        $incorrect_message.removeClass("invisible");
    }

    $next_button.removeClass("invisible");
    $submit_button.addClass("invisible");
}