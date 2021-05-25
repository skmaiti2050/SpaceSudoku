function setInputFilter(textbox, inputFilter) {
	["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function (event) {
		textbox.addEventListener(event, function () {
			if (inputFilter(this.value)) {
				this.oldValue = this.value;
				this.oldSelectionStart = this.selectionStart;
				this.oldSelectionEnd = this.selectionEnd;
			} else if (this.hasOwnProperty("oldValue")) {
				this.value = this.oldValue;
				this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
			} else {
				this.value = "";
			}
		});
	});
}

$(document).on("keydown", ".Input", function () {
	setInputFilter(this, function (value) {
		return /^\d*$/.test(value) && (value === '' || parseInt(value) > 0 && parseInt(value) <= 9);
	});
});

let newgame = "true";
var res1 = null;
var res2 = null;
let list = ["A", "B", "C", "D", "E", "F", "G", "H", "I"];

document.getElementById("alert_info").style.display = "block";

function checkBlank(row, c) {
	if ($(c).val() == "") {
		row.push("0");
	} else {
		row.push($(c).val());
	}
}

function pushValue(row, c) {
	if (c == "") {
		row.push("0");
	} else {
		row.push(c);
	}
}

cell = []
var c,
	row1 = [],
	row2 = [],
	row3 = [],
	row4 = [],
	row5 = [],
	row6 = [],
	row7 = [],
	row8 = [],
	row9 = [];

for (i in list) {
	for (j = 1; j <= 9; j++) {
		c = '#cell_' + list[i] + j;
		cell.push(c)
		if (list[i] == "A") {
			checkBlank(row1, c);
		} else if (list[i] == "B") {
			checkBlank(row2, c);
		} else if (list[i] == "C") {
			checkBlank(row3, c);
		} else if (list[i] == "D") {
			checkBlank(row4, c);
		} else if (list[i] == "E") {
			checkBlank(row5, c);
		} else if (list[i] == "F") {
			checkBlank(row6, c);
		} else if (list[i] == "G") {
			checkBlank(row7, c);
		} else if (list[i] == "H") {
			checkBlank(row8, c);
		} else if (list[i] == "I") {
			checkBlank(row9, c);
		}
	};
};

function checkSolution() {

	var ct,
		r1 = [],
		r2 = [],
		r3 = [],
		r4 = [],
		r5 = [],
		r6 = [],
		r7 = [],
		r8 = [],
		r9 = [];

	for (i in list) {
		for (j = 1; j <= 9; j++) {
			ct = 'cell_' + list[i] + j;
			if (list[i] == "A") {
				pushValue(r1, res1[ct]);
			} else if (list[i] == "B") {
				pushValue(r2, res1[ct]);
			} else if (list[i] == "C") {
				pushValue(r3, res1[ct]);
			} else if (list[i] == "D") {
				pushValue(r4, res1[ct]);
			} else if (list[i] == "E") {
				pushValue(r5, res1[ct]);
			} else if (list[i] == "F") {
				pushValue(r6, res1[ct]);
			} else if (list[i] == "G") {
				pushValue(r7, res1[ct]);
			} else if (list[i] == "H") {
				pushValue(r8, res1[ct]);
			} else if (list[i] == "I") {
				pushValue(r9, res1[ct]);
			}
		};
	};

	req = $.ajax({
		type: 'POST',
		url: '/solvesudoku',
		data: {
			row1: JSON.stringify(r1),
			row2: JSON.stringify(r2),
			row3: JSON.stringify(r3),
			row4: JSON.stringify(r4),
			row5: JSON.stringify(r5),
			row6: JSON.stringify(r6),
			row7: JSON.stringify(r7),
			row8: JSON.stringify(r8),
			row9: JSON.stringify(r9),
		},
		success: function (data) {
			res2 = Object.values(data);
		}
	});
}

var isSolved = false

function newGame() {
	resetTime();
	$("#overlay").css({
		"display": "none"
	})
	$("#loader").css({
		"display": "block"
	})

	for (i = 0; i < 81; i++) {
		a = $(".Input")[i]
		$(a).addClass("pause")
	}

	req = $.ajax({
		type: 'POST',
		url: '/',
		data: {
			level: $('#slct option:selected').text(),
		},
		success: function (data) {
			res1 = data;
			while (res1 != null && !isSolved) {
				checkSolution();
				isSolved = true
			}
		}
	});

	req.done(function (data) {
		var i = 0;
		for (j in data) {
			if (data[j] == "0") {
				$(cell[i]).val('');
				$(cell[i]).removeClass("black");
				$(cell[i]).removeAttr('readonly');
			} else {
				$(cell[i]).val(data[j]);
				$(cell[i]).attr('readonly', 'readonly');
				$(cell[i]).addClass("black")
			};
			i++;
		};

		$("#loader").css({
			"display": "none"
		})
		for (i = 0; i < 81; i++) {
			a = $(".Input")[i]
			$(a).removeClass("pause")
		}
		start();
		isSolved = false
	});
}

$(document).on("click", "#playButton", function () {
	if (elapsedTime == 0) {
		newGame();
	}
	if (status === "stopped") {
		status = "started";
		return true;
	} else {
		return false
	}
});

$(document).on("click", "#resetButton", function () {
	$('input').val('');
	pause();
	resetTime();
});

$(document).on("click", "#check_sol", function () {
	var temp = [];
	var empty = $("input").filter(function () {
		return this.value === ""
	})
	if (empty.length > 0) {
		$("#alert").css({
			"display": "block"
		})
		pause();
	} else {
		var inputs = $("input");
		for (var i = 0; i < inputs.length; i++) {
			if ($(inputs[i]).val() == "") {
				temp.push(0)
			} else {
				temp.push(parseInt($(inputs[i]).val()));
			}
		}
		if (JSON.stringify(temp) === JSON.stringify(res2)) {
			document.getElementById("alert_success").style.display = "block";
			pause();
			for (i = 0; i < 81; i++) {
				a = $(".Input")[i]
				$(a).removeClass("pause")
			}
			document.getElementById("overlay").style.display = "none";
		} else {
			document.getElementById("alert_warning").style.display = "block";
			on();
		}
	}
});

$(document).on("click", "#show_sol", function() {
    var c_empty = $("input").filter(function () {
		return this.value === ""
	})
	if (c_empty.length < 81) {
		$("#loader").css({ "display": "block" })
		var i = 0;
		for (j in res2) {
			$(cell[i]).val(res2[j])
			i++;
		}
		$("#loader").css({ "display": "none" })
		pause();
		for (i = 0; i < 81; i++) {
			a = $(".Input")[i]
			$(a).removeClass("pause")
		}
		document.getElementById("overlay").style.display = "none";
		resetTime();
	}	
	document.getElementById("alert_play").style.display = "block";
});

$(document).on("focus", ".Input", function () {
	clas = this.className;
	var classlist = clas.split(" ");

	$("." + classlist[1]).addClass("active");
	$("." + classlist[2]).addClass("active");
	$("." + classlist[3]).addClass("active");
	$(this).addClass("focused")

});

$(document).on("blur", ".Input", function () {
	clas = this.className;
	var classlist = clas.split(" ");

	$("." + classlist[0]).removeClass("active");
	$("." + classlist[1]).removeClass("active");
	$("." + classlist[2]).removeClass("active");
	$(this).removeClass("focused")
});

let status = "stopped";

function timeToString(time) {
	let diffInHrs = time / 3600000;
	let hh = Math.floor(diffInHrs);

	let diffInMin = (diffInHrs - hh) * 60;
	let mm = Math.floor(diffInMin);

	let diffInSec = (diffInMin - mm) * 60;
	let ss = Math.floor(diffInSec);

	let diffInMs = (diffInSec - ss) * 100;
	let ms = Math.floor(diffInMs);

	let formattedMM = mm.toString().padStart(2, "0");
	let formattedSS = ss.toString().padStart(2, "0");
	let formattedMS = ms.toString().padStart(2, "0");

	return `${formattedMM}:${formattedSS}:${formattedMS}`;
}

let startTime;
let elapsedTime = 0;
let timerInterval;

function print(txt) {
	document.getElementById("display").innerHTML = txt;
}

function start() {
	startTime = Date.now() - elapsedTime;
	timerInterval = setInterval(function printTime() {
		elapsedTime = Date.now() - startTime;
		print(timeToString(elapsedTime));
	}, 10);
	showButton("PAUSE");
	if (status === "stopped") {
		status = "started";
		off()
		return true;
	} else {
		return false
	}
}

function pause() {
	clearInterval(timerInterval);
	showButton("PLAY");
	if (status === "started") {
		status = "stopped"
		on();
		return true;
	} else {
		return false
	}
}

function resetTime() {
	clearInterval(timerInterval);
	print("00:00:00");
	elapsedTime = 0;
	showButton("PLAY");
	status = "stopped"
}

function showButton(buttonKey) {
	const buttonToShow = buttonKey === "PLAY" ? playButton : pauseButton;
	const buttonToHide = buttonKey === "PLAY" ? pauseButton : playButton;
	buttonToShow.style.display = "block";
	buttonToHide.style.display = "none";
}

let playButton = document.getElementById("playButton");
let pauseButton = document.getElementById("pauseButton");
let resetButton = document.getElementById("resetButton");

playButton.addEventListener("click", start);
pauseButton.addEventListener("click", pause);
resetButton.addEventListener("click", resetTime);

function on() {
	document.getElementById("overlay").style.display = "block";
	pause();

	for (i = 0; i < 81; i++) {
		a = $(".Input")[i]
		$(a).addClass("pause")
	}
}

function off() {
	document.getElementById("overlay").style.display = "none";
	if (status == "stopped") {
		start();
	}

	for (i = 0; i < 81; i++) {
		a = $(".Input")[i]
		$(a).removeClass("pause")
	}

	if (newgame == "true") {
		$("#resetButton").trigger("click");
		newgame = "false"
	}
}

$(document).keydown(function (e) {
	var $table = $(this);
	var $active = $('input:focus,select:focus', $table);
	var $next = null;
	var focusableQuery = 'input:visible,select:visible,textarea:visible';
	var position = parseInt($active.closest('td').index()) + 1;
	switch (e.keyCode) {
		case 37:
			$next = $active.parent('td').prev().find(focusableQuery);
			break;
		case 38:
			$next = $active
				.closest('tr')
				.prev()
				.find('td:nth-child(' + position + ')')
				.find(focusableQuery);
			break;
		case 39:
			$next = $active.closest('td').next().find(focusableQuery);
			break;
		case 40:
			$next = $active
				.closest('tr')
				.next()
				.find('td:nth-child(' + position + ')')
				.find(focusableQuery);
			break;
	}
	if ($next && $next.length) {
		$next.focus();
	}
});