import { makeToastNotification } from "/static/helper.js"

class Review {
    constructor(lengthOfQuiz) {
        this.lengthOfQuiz = lengthOfQuiz
        this.answeredQuestionsCount = 0
    }

    addAnsweredQuestions() {
        this.answeredQuestionsCount++
    }

    reduceAnsweredQuestions() {
        this.answeredQuestionsCount--
    }

    peek() {
        return this.answeredQuestionsCount
    }

}

document.querySelectorAll(".question").forEach(question => {
    question.innerHTML = question.innerHTML.replace(/'/g, '"')
})

document.querySelectorAll(".choice").forEach(choice => { choice.classList.add("hoverable") })

const review = new Review(document.getElementById("length-of-quiz").value)

$(document).ready(function() {

    $(document).on("click", ".choice", function() {

        if ($(this).siblings(".chose").length > 0) {
            makeToastNotification("Clear answer first")
            return false
        }
        const link = $(this).attr("data-link");
        const choice_id = $(this).attr("data-choice-id")
        const question_id = $(this).attr("data-question-id")
        const question_type = $(this).attr("data-type")

        let request = $.post(link, {
            question_id: question_id,
            choice_id: choice_id,
            question_type: question_type
        })

        request.done(function(data) {
            makeToastNotification(data)
        })
        request.fail(function() {
            makeToastNotification("Failed to record answer")
        })

        review.addAnsweredQuestions()
        $(this).addClass("chose")
        $(this).parent().parent().find(".clear-answer").addClass("active")
        $(this).parent().parent().find(".clear-answer").attr("data-choice-id", choice_id)
        $(this).parent().parent().find(".clear-answer").attr("data-question-id", question_id)

    })

    $(document).on("click", ".clear-answer", function() {
        if ($(this).attr("data-type") == "multiple-choice") {
            const link = $(this).attr("data-link");
            const choice_id = $(this).attr("data-choice-id")
            const question_id = $(this).attr("data-question-id")

            let request = $.post(link, {
                question_id: question_id,
                choice_id: choice_id,
            })

            request.done(function(data) {
                makeToastNotification(data)
            })
            request.fail(function() {
                makeToastNotification("Failed to remove answer")
            })

            review.reduceAnsweredQuestions()
            $(this).siblings(".choices-container").find(".chose").removeClass("chose")
        }
    })
})