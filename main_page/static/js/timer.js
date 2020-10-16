$(document).ready(function () {
    function Timer(fn, interval) {
        var id = setInterval(fn, interval);
        this.cleared = false;
        this.clear = function () {
            this.cleared = true;
            clearInterval(id);
        };
    }

    function displayTimer(milliseconds) {
        var hours = Math.floor(milliseconds / 3600000);
        var minutes = Math.floor((milliseconds - hours * 3600000) / 60000);
        var seconds = Math.floor((milliseconds - hours * 3600000 - minutes * 60000) / 1000);
        if (hours < 10) hours = "0" + hours;
        if (minutes < 10) minutes = "0" + minutes;
        if (seconds < 10) seconds = "0" + seconds;
        return hours + ":" + minutes + ":" + seconds;
    }

    var start = false;

    $("#timer")[0].innerHTML = displayTimer($("#timer")[0].dataset.defaultMilliseconds);
    $("#timer")[0].setAttribute('data-current-milliseconds', $("#timer")[0].dataset.defaultMilliseconds);

    $("#start").on("click", function () {
        $("#start")[0].innerHTML = "Restart";
        $("#start")[0].classList.remove('btn-primary', 'btn-info');
        $("#start")[0].classList.add('btn-warning');
        if (!start) {
            start = true;
            milliseconds = $("#timer")[0].dataset.currentMilliseconds;
            timer = new Timer(function () {
                milliseconds -= 1000;
                if (milliseconds == 0) {
                    $("#start")[0].innerHTML = "Start";
                    $("#start")[0].classList.remove('btn-warning', 'btn-info');
                    $("#start")[0].classList.add('btn-primary');
                    $("#timer")[0].setAttribute('data-current-milliseconds', $("#timer")[0].dataset.defaultMilliseconds);
                    milliseconds = $("#timer")[0].dataset.defaultMilliseconds;
                    timer.clear();
                    start = false;
                    var filename = "/static/sound/poppy_-_time-is-up";
                    var block = document.createElement('div');
                    $(".container-for-timer")[0].appendChild(block);
                    block.innerHTML = '<audio autoplay><source src="' + filename + '.mp3" type="audio/mpeg" /><source src="' + filename + '.ogg" type="audio/ogg" /><embed hidden="true" autostart="true" loop="false" src="' + filename + '.mp3" /></audio>';
                }
                $("#timer")[0].innerHTML = displayTimer(milliseconds)
            }, 1000)
        } else {
            $("#timer")[0].innerHTML = displayTimer($("#timer")[0].dataset.defaultMilliseconds);
            timer.clear();
            start = false;
            start = true;
            milliseconds = $("#timer")[0].dataset.defaultMilliseconds;
            timer = new Timer(function () {
                milliseconds -= 1000;
                if (milliseconds == 0) {
                    timer.clear();
                }
                $("#timer")[0].innerHTML = displayTimer(milliseconds)
            }, 1000)
        }
    })

    $("#pause").on("click", function () {
        if ($("#start")[0].innerHTML == "Restart") {
            timer.clear();
            $("#timer")[0].setAttribute('data-current-milliseconds', milliseconds);
            $("#start")[0].innerHTML = "Continue";
            $("#start")[0].classList.remove('btn-warning', 'btn-primary');
            $("#start")[0].classList.add('btn-info')
            $("#timer")[0].innerHTML = displayTimer($("#timer")[0].dataset.currentMilliseconds);
            start = false;
        } else {
            alert("Wrong");
            return;
        }
    })

    $("#stop").on("click", function () {
        if ($("#start")[0].innerHTML == "Restart" || $("#start")[0].innerHTML == "Continue") {
            $("#start")[0].innerHTML = "Start";
            $("#start")[0].classList.remove('btn-warning', 'btn-info');
            $("#start")[0].classList.add('btn-primary');
            $("#timer")[0].innerHTML = displayTimer($("#timer")[0].dataset.defaultMilliseconds);
            $("#timer")[0].setAttribute('data-current-milliseconds', $("#timer")[0].dataset.defaultMilliseconds);
            var was_milliseconds = $("#timer")[0].dataset.defaultMilliseconds - milliseconds;
            this.parentNode.children[3].setAttribute('href', this.parentNode.children[3].getAttribute('href') + was_milliseconds);
            milliseconds = $("#timer")[0].dataset.defaultMilliseconds;
            timer.clear();
            start = false;
            this.parentNode.children[3].click();
        } else {
            alert("Wrong");
            return;
        }
    })
});