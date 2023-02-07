"use strict";

let domReady = (cb) => {
  document.readyState === 'interactive' || document.readyState === 'complete'
    ? cb()
    : document.addEventListener('DOMContentLoaded', cb);
};

domReady(() => {
  // Display body when DOM is loaded
  document.body.style.visibility = 'visible';
  insertContent();
});

var App = window.App || {};

!(function () {
    var n = $("html"),
        t = function () {
            $(".btn-menu").on("click", function (t) {
                t.preventDefault(), n.toggleClass("menu-opened");
            });
        },
        e = function () {
            t();
        };
    e();
})();

// various functions used in scripts in this site

function getQueryVariable(variable)
{
   var query = window.location.search.substring(1);
   var vars = query.split("&");
   for (var i=0;i<vars.length;i++) {
           var pair = vars[i].split("=");
           if(pair[0] == variable){return decodeURIComponent(pair[1]);}
   }
   return(false);
}

function fadeout(element) {
    var op = 1;  // initial opacity
    var timer = setInterval(function () {
        if (op <= 0.1){
            clearInterval(timer);
            op = 0;
            //element.style.display = 'none';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 20);
}

function fadein(element) {
    var op = 0.1;  // initial opacity
    //element.style.display = 'block';
    var timer = setInterval(function () {
        if (op >= 1){
            clearInterval(timer);
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.1;
    }, 20);
}
var titleEnd = 'App';

function requestAPI() {
    $.ajax({
        method: 'GET',
        url: '/cgi-bin/api.py',
        contentType: 'application/json',
        dataType : "json",
        success: completeRequest,
        error: function ajaxError(jqXHR, textStatus, errorThrown) {
            console.error('Error requesting API data: ', textStatus, ', Details: ', errorThrown);

            var outStr = '';

			try{
			    outStr = jqXHR.responseJSON.message;
                console.error('Response: ', jqXHR.responseText);
	        }
			catch(err){
                outStr = 'Unknown Error';
		    }
			finally{
                $("#ajaxInsert").replaceWith('<div id="ajaxInsert"><p style="text-align:center;">An error occured when requesting API data:<br>\n' + outStr + '</p></div>');
                $("title").replaceWith('<title>Error | '+titleEnd+'</title>');
                window.scrollTo(0, 0);
            }
        }
    });
}

function completeRequest(result) {
	var articleTopIns = '';
	if (result.title) {
		articleTopIns = '<h2 style="text-align:center;">'+
		  result.error+'</h2>\n<p style="text-align:center;">'+result.status_code+'</p>\n';
    }
	$("#ajaxInsert").replaceWith('<div id="ajaxInsert">\n'+articleTopIns+
	  result.results.description+'\n</div>');
    $("title").replaceWith('<title>'+titleEnd+'</title>');
    window.scrollTo(0, 0);
}

function insertContent() {
   	$("title").replaceWith('<title>Loading... | '+titleEnd+'</title>');
   	$("#ajaxInsert").replaceWith('<div id="ajaxInsert"><p style="text-align:center;">Loading...</p></div>');
    requestAPI();
}

function replaceContent() {
    //fadeout(document.getElementById('main'));
	$("title").replaceWith('<title>Loading... | '+titleEnd+'</title>');
   	$("#ajaxInsert").replaceWith('<div id="ajaxInsert"><p style="text-align:center;">Loading...</p></div>');
    history.pushState(null, null, '/search.html');
}

window.onpopstate = function(e) {
    insertContent();
};
