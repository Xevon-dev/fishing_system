
const questions = document.querySelectorAll(".question-slide");
const next = document.querySelector("#next-button");
const back = document.querySelector("#back-button");
const error = document.querySelector("#answer-error");

let index = 0;

function showQuestion() {
    for (let i = 0; i < questions.length; i++) {
        questions[i].hidden = true;
    }

    questions[index].hidden = false;
    error.textContent = "";

    document.querySelector("#question-count").textContent =
        "Питання " + (index + 1) + " з " + questions.length;

    let percent = Math.round((index + 1) / questions.length * 100);

    document.querySelector("#progress-label").textContent = percent + "%";
    document.querySelector("#progress-fill").style.width = percent + "%";

    back.disabled = index === 0;

    if (index === questions.length - 1) {
        next.textContent = "Показати результат →";
    } else {
        next.textContent = "Далі →";
    }
}

if (questions.length > 0) {
    next.onclick = function() {
        let answer = questions[index].querySelector("input:checked");

        if (!answer) {
            error.textContent = "Оберіть один із варіантів відповіді";
            return;
        }

        error.textContent = "";

        if (index < questions.length - 1) {
            index++;
            showQuestion();
        } else {
            document.querySelector("#test-card").submit();
        }
    };

    back.onclick = function() {
        if (index > 0) {
            index--;
            showQuestion();
        }
    };

    showQuestion();
}
