console.log('executing viewPost.js file')
//var csvFile;
//groupMouseClicksAndSendJson();

var date = new Date();
var timestamp = date.getTime();
var csrf;
var dictJson = {}
var mouseClickArray = []
var scrollArray = []
var parameters;

function setcsrf(csr){
	csrf = csr
}



function getQueryRecommendation(query){
	const url1 = 'http://127.0.0.1:8000/discussions/getQueryRecommendation'
	$.ajax({
		type: "POST",
		url: url1,
		data: {
			query: query,
			csrfmiddlewaretoken: csrf
		},
		success: function(data) {
			parameters = data;
			mp = JSON.parse(data);

			for (var i = 0 ;i< 10;i++){
				var tmp = "rec"+(i+1)
				var acc = "acc"+(i+1)
				document.getElementById(tmp).innerHTML = mp[i]["content"];
				document.getElementById(acc).innerHTML = mp[i]["topic"];
			}
			hideUnhide("outputField",true)
			console.log("Success")
		}
	})
}


function hideUnhide(id,flag) {
	console.log('hideUnhide called'+id)
	var x = document.getElementById(id);
	if (flag == true){
		x.style.display = "block";
	}
	else if (x.style.display === "none") {
		x.style.display = "block";
	} else {
		x.style.display = "none";
	}
}

