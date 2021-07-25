const $choiceForm = $("#choice-form");
const $correct_name = $("#correct_name")
const $result = $("#result")
const $next_button = $("#next_button")
const $submit_button = $("#submit_button")

$choiceForm.on("submit", checkAnswer);

function checkAnswer(evt) {
    evt.preventDefault();
    let choice = $choiceForm.serializeArray()[0]["value"];
    let correct_name = $correct_name.text();
    choice = choice.replace(/[\n\r]/g, '').replace(/\s+/g,"");
    correct_name = correct_name.replace(/[\n\r]/g, '').replace(/\s+/g,"");

    if(choice === correct_name){
        $result.removeClass("invisible");
        $result.removeClass("bg-danger");
        $result.addClass("bg-success");
        $result.text("CORRECT!");
    }
    else{
        $result.removeClass("invisible");
        $result.removeClass("bg-success");
        $result.addClass("bg-danger");
        $result.text("INCORRECT!");
    }

    $next_button.removeClass("invisible");
    $submit_button.addClass("invisible");
}