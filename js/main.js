"use strict";

// Site title, put at end of title attribute on all pages
var titleEnd = 'Game Rental Demo';

// Code to do some setup when page finishes loading
let domReady = (cb) => {
    document.readyState === 'interactive' || document.readyState === 'complete'
      ? cb()
      : document.addEventListener('DOMContentLoaded', cb);
  };
  
  domReady(() => {
    // Display search results or other data when DOM is loaded if parameter given
    if (getQueryVariable('gameId') !== false) {
        if (getQueryVariable('checkout') != false) { // If both gameId and checkout are set, you're in the checkout stage
            insertContent('', getQueryVariable('gameId'), getQueryVariable('checkout'));
        } else { // If gameId is set without checkout, you're in the game details page
            insertContent('', getQueryVariable('gameId'), '');
        }
    } else if (getQueryVariable('searchStr') !== false) { // If searchStr is set and none of the others, you're in search results
        insertContent(getQueryVariable('searchStr'), '', '');
    }
  });
  
// Some code for a navigation menu that isn't currently used but might be in the future
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

// Get variables out of URL query string
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

// Fade effects not currently used
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

// AJAX routines to get data from our Python script that in turn gets it from the remote API
function retrieveApiContent(searchStr, gameId, checkout) {
    $.ajax({
        method: 'GET',
        url: 'cgi-bin/api.py?searchStr='+encodeURIComponent(searchStr)+'&gameId='+encodeURIComponent(gameId)+'&checkout='+encodeURIComponent(checkout),
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
                outStr = textStatus+': '+errorThrown;
		    }
			finally{
                $("#ajaxInsert").replaceWith('<div id="ajaxInsert"><p style="text-align:center;">An error occured when requesting API data:<br>\n' + outStr + '</p></div>');
                $("title").replaceWith('<title>Error | '+titleEnd+'</title>');
                window.scrollTo(0, 0);
            }
        }
    });
}

// When request completes, insert the returned data in the appropriate place, and change the page title
function completeRequest(result) {
	$("#ajaxInsert").replaceWith('<div id="ajaxInsert">\n'+
      '<h2>'+result.title+'</h2>'+
	  result.body+'\n</div>');
    $("title").replaceWith('<title>'+result.title+' | '+titleEnd+'</title>');
    window.scrollTo(0, 0);
}

// Called when you want to load data from the API and replace it on the page without altering the history stack
function insertContent(searchStr, gameId, checkout) {
   	//$("title").replaceWith('<title>Loading... | '+titleEnd+'</title>');
   	$("#ajaxInsert").replaceWith('<div id="ajaxInsert"><p style="text-align:center;">Loading...</p></div>');
    retrieveApiContent(searchStr, gameId, checkout);
}

// Called to load data from the API, display it, and add to the history stack so you can use the back button
function newContentPage(searchStr, gameId, checkout) {
    history.replaceState({'searchStr': searchStr, 'gameId': gameId, 'checkout': checkout}, '');
    insertContent(searchStr, gameId, checkout);
    if (gameId) {
        if (checkout) {
            history.pushState({'searchStr': searchStr, 'gameId': gameId, 'checkout': checkout}, '', '/?gameId='+encodeURIComponent(gameId)+'&checkout='+encodeURIComponent(checkout));
        } else {
            history.pushState({'searchStr': searchStr, 'gameId': gameId, 'checkout': checkout}, '', '/?gameId='+encodeURIComponent(gameId));
        }
    } else {
        history.pushState({'searchStr': searchStr, 'gameId': gameId, 'checkout': checkout}, '', '/?searchStr='+encodeURIComponent(searchStr));
    }
}

// When you use the back button, restore the past state appropriately, including page title.
window.onpopstate = function(e) {
    if (getQueryVariable('gameId') !== false) {
        if (getQueryVariable('checkout') !== false) {
            insertContent('', getQueryVariable('gameId'), getQueryVariable('checkout'));
        } else {
            insertContent('', getQueryVariable('gameId'), '');
        }
    } else if (getQueryVariable('searchStr') !== false) {
        insertContent(getQueryVariable('searchStr'), '', '');
    } else {
        $("#ajaxInsert").replaceWith('<div id="ajaxInsert">\n'+'</div>');
        $("title").replaceWith('<title>'+titleEnd+'</title>');
    }
    if (e.state && e.state.searchStr) {
        $("#searchField").val(e.state.searchStr);
    } else {
        $("#searchField").val('')
    }
};
