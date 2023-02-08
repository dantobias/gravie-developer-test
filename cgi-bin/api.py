#!/usr/bin/python3

import urllib.request
import json
import html
import urllib.parse
import cgi

apiurl = 'https://www.giantbomb.com/api'
apikey = '9f5f504612747bac723f6776a7e63514959350e2'

def do_checkout(gameid, platformSel):
    url = apiurl+'/game/'+urllib.parse.quote_plus(gameid)+'/?api_key='+apikey+'&format=json'

    try:
        page = urllib.request.urlopen(url)
        rawdata = page.read()
        indata = json.loads(rawdata.decode('ascii'))

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
        else:
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

        if 'description' in indata['results'] and indata['results']['description']:
            body += indata['results']['description']
        elif 'deck' in indata['results'] and indata['results']['deck']:
            body += '<p>'+indata['results']['deck']+'</p>'

        if 'platforms' in indata['results'] and indata['results']['platforms']:
            platformStr = ''
            for platform in indata['results']['platforms']:
                if 'name' in platform:
                    if platformStr:
                        platformStr += ', '
                    platformStr += platform['name']
            body += '<p><b>Platforms:</b> '+platformStr+'</p>\n'

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

        result = {'title': title, 'body': body}
        return json.dumps(result)
    except:
        return json.dumps({'title': 'Unable to handle request', 'body': '<p>Either there is a problem with the system that handles game searches, or you have entered an improper query.</p>'})

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
