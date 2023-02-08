#!/usr/bin/python3

import urllib.request
import json
import html
import urllib.parse
import cgi
import re

apiurl = 'https://www.giantbomb.com/api'
apikey = '9f5f504612747bac723f6776a7e63514959350e2'

# Handles checkout. The 'checkout' parameter from elsewhere is passed here as 'platformSel' where it stores the
# selected platform if it's greater than zero, while -1 is used to signal the initial checkout page where you
# have to choose a platform. In an actual production site, there'd need to be more data structures to store
# such things as user data so it knows who to send the games to, and perhaps a shopping cart to let you choose
# multiple games before you check out, and billing data (whether per-game or monthly subscription or whatever)
# with a database to store all of that in, but this is just a simple demo without that stuff.

def do_checkout(gameid, platformSel):
    url = apiurl+'/game/'+urllib.parse.quote_plus(gameid)+'/?api_key='+apikey+'&format=json'

    try:
        page = urllib.request.urlopen(url)
        rawdata = page.read()
        indata = json.loads(rawdata.decode('ascii'))

        # First checkout page
        if int(platformSel) < 0:        
            title = 'Checkout: '+indata['results']['name']
            body = '<p><a href="javascript:history.back();">&#8592;Go Back</a></p>\n'
            body += '<div class="checkout">\n'

            body += '<p><b>Item #:</b> '+indata['results']['guid']+'</p>\n'

            if 'deck' in indata['results'] and indata['results']['deck']:
                body += '<p>'+indata['results']['deck']+'</p>'

            body += '<p>You are completing your checkout for a game rental of '+indata['results']['name']+'.</p>\n'

            if 'platforms' in indata['results'] and indata['results']['platforms']:
                platformStr = '<select name="platform" id="platformField">'
                for platform in indata['results']['platforms']:
                    if 'name' in platform:
                        platformStr += '<option value="'+str(platform['id'])+'">'+platform['name']+'</option>'
                platformStr += '</select>\n'
                body += '<p><b>Please select the desired platform:</b> '+platformStr+'</p>\n'

            body += '<button onClick="newContentPage(\'\', \''+indata['results']['guid']+'\', $(\'#platformField\').val())">Complete your Checkout</button>\n'

            body += '</div>\n'
        else:  # Second checkout page; final completion
            title = 'Completed Checkout: '+indata['results']['name']
            body = '<div class="checkoutcomplete">\n'

            platformStr = 'Unknown Platform'
            if 'platforms' in indata['results'] and indata['results']['platforms']:
                for platform in indata['results']['platforms']:
                    if int(platform['id']) == int(platformSel):
                        platformStr = platform['name']

            body += '<p>You have completed your checkout for a game rental of '+indata['results']['name']+' for the '+platformStr+'.</p>\n'
            body += '<p>You would be receiving it shortly, if this site actually worked as a game rental site rather than just a test exercise.</p>\n'
            body += '<p><a href="/">Return Home</a></p>\n'

            body += '</div>\n'

        result = {'title': title, 'body': body}
        return json.dumps(result)
    except:
        return json.dumps({'title': 'Unable to handle request', 'body': '<p>There is a problem with the system that handles game detail requests, preventing the completion of this checkout. Please try again later.</p>'})

# Load and isplay info on one game

def game_info(gameid):
    url = apiurl+'/game/'+urllib.parse.quote_plus(gameid)+'/?api_key='+apikey+'&format=json'

    try:
        page = urllib.request.urlopen(url)
        rawdata = page.read()
        indata = json.loads(rawdata.decode('ascii'))

        title = 'Game Details: '+indata['results']['name']
        body = '<p><a href="javascript:history.back();">&#8592;Go Back</a></p>\n'
        body += '<div class="itemdetails">\n'
        if 'super_url' in indata['results']['image'] and indata['results']['image']['super_url']:
            body += '<div style="text-align:center;"><img src="'+indata['results']['image']['super_url']+'" alt="[Game Image]" style="width:90%; height:auto; margin:auto;"></div>\n'

        body += '<p><b>Item #:</b> '+indata['results']['guid']+'</p>\n'

        descStr = ''
        if 'description' in indata['results'] and indata['results']['description']:
            descStr = indata['results']['description']
        elif 'deck' in indata['results'] and indata['results']['deck']:
            descStr = '<p>'+indata['results']['deck']+'</p>'

        # Strip hyperlinks from description because they don't work
        descStr = re.sub("<(a [^>]*|/a)>", "", descStr)

        body += descStr

        if 'platforms' in indata['results'] and indata['results']['platforms']:
            platformStr = ''
            for platform in indata['results']['platforms']:
                if 'name' in platform:
                    if platformStr:
                        platformStr += ', '
                    platformStr += platform['name']
            body += '<p><b>Platforms:</b> '+platformStr+'</p>\n'

        if 'publishers' in indata['results'] and indata['results']['publishers']:
            publisherStr = ''
            for publisher in indata['results']['publishers']:
                if 'name' in publisher:
                    if publisherStr:
                        publisherStr += ', '
                    publisherStr += publisher['name']
            body += '<p><b>Publishers:</b> '+publisherStr+'</p>\n'

        if 'original_game_rating' in indata['results'] and indata['results']['original_game_rating']:
            ratingStr = ''
            for rating in indata['results']['original_game_rating']:
                if 'name' in rating:
                    if ratingStr:
                        ratingStr += ', '
                    ratingStr += rating['name']
            body += '<p><b>Ratings:</b> '+ratingStr+'</p>\n'

        body += '<button onClick="newContentPage(\'\', \''+indata['results']['guid']+'\', \'-1\')">Rent It</button>\n'

        body += '</div>\n'

        result = {'title': title, 'body': body}
        return json.dumps(result)
    except:
        return json.dumps({'title': 'Unable to handle request', 'body': '<p>There is a problem with the system that handles game detail requests.</p>'})

# Load and display game search results

def game_search(searchStr):
    url = apiurl+'/search/?api_key='+apikey+'&format=json&query="'+ urllib.parse.quote_plus(searchStr)+'"&resources=game'

    try:
        page = urllib.request.urlopen(url)
        rawdata = page.read()
        indata = json.loads(rawdata.decode('ascii'))

        title = 'Search Results: '+html.escape(searchStr)
        body = ''

        for item in indata['results']:
            body += '<div class="searchitem">'
            body += '    <div class="itemthumb">'
            if 'image' in item and item['image']:
                if 'thumb_url' in item['image'] and item['image']['thumb_url']:
                    body += '        <img src="'+item['image']['thumb_url']+'" alt="[Game Thumbnail Image]" style="width:100%; height:auto;">'
            body += '    </div>\n'
            body += '    <div class="itemdetail">'
            body += '        <h3 style="margin-top:0; padding-top:0;">'+html.escape(item['name'])
            body += '            <span style="font-size:0.8em; font-weight:normal;">(Item #'+html.escape(item['guid'])+')</span></h3>\n'
            if 'deck' in item and item['deck']:
                body += '    <p>'+html.escape(item['deck'])+'</p>\n'
            if 'platforms' in item and item['platforms']:
                platformStr = ''
                for platform in item['platforms']:
                    if 'name' in platform:
                        if platformStr:
                            platformStr += ', '
                        platformStr += platform['name']
                body += '<p><b>Platforms:</b> '+platformStr+'</p>\n'
            body += '        <button onClick="newContentPage(\'\', \''+item['guid']+'\', \'\')">Details</button> <button onClick="newContentPage(\'\', \''+item['guid']+'\', \'-1\')">Rent It</button>\n'
            body += '    </div>\n'
            body += '    <br style="clear:left;">'
            body += '</div>\n'

        if body == '':
            body = '<p>No results were found for this search.</p>\n'

        result = {'title': title, 'body': body}
        return json.dumps(result)
    except:
        return json.dumps({'title': 'Unable to handle request', 'body': '<p>Either there is a problem with the system that handles game searches, or you have entered an improper query.</p>'})

# Get CGI parameters

arguments = cgi.parse()
searchStr = ''
if ('searchStr' in arguments):
    searchStr = arguments['searchStr'][0]
gameId = ''
if ('gameId' in arguments):
    gameId = arguments['gameId'][0]
checkout = ''
if ('checkout' in arguments):
    checkout = arguments['checkout'][0]

# Get appropriate results and send them as JSON
# In all cases, JSON has structure with title and body values so JavaScript routines can consistently display them.

print("Content-type: application/json\n\n")
if gameId:
    if checkout:
        print(do_checkout(gameId, checkout))
    else:
        print(game_info(gameId))
elif searchStr:
    print(game_search(searchStr))
else:
    print(json.dumps({'title': 'No search string given', 'body': '<p>You need to enter something to search for.</p>'}))
