# Caroline Gallagher
# musicwebpagewriter.py
# Written Feb 12, 2012
# Edited Sept 24, 2012 by Caroline Gallagher

import urllib2
import json
import os

# Reformats the song title so that it can be used as the .html address, by inserting '+'
# between each word
def formatParam (param):
    pList = param.split()
    param = pList[0]
    
    for i in range(1,len(pList)):
        param = param + "+" + pList[i]

    return param

# Returns the header of the webpage, with a title corresponding
# to the name of the track.
def writeFirstPart(title):
    firstPart = \
    """
    <html class="no-js">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>%s</title>

    <link rel="stylesheet" href="css/reset.css" media="screen" />
    <link rel="stylesheet" href="css/style.css" media="screen" />
    <link rel="stylesheet" href="css/css3_3d.css" media="screen" />

    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
    <script type="text/javascript" src="js/modernizr.js"></script>

    <script>

    if (!Modernizr.csstransforms) {
    	$(document).ready(function(){
			$(".close").text("Back to top");
				});
				}
				</script>

				</head>""" %(title)
    
    return firstPart

# Creates the box with the image and artist name for each song.
# If the user clicks the box, then the user will see more information
# about that song.
def writeDetails(entryDct, link,n):
    if n%3 == 0:
        li = "li class='end'"
    else:
        li = "li"
        
    detail = \
        """
        <%s>
                <div class="details">
                	<h3>%s</h3>
                    <a class="more" href=#%s>view details</a> 
                </div>
               <a href=#%s><img src="%s" alt = %s/></a>
            </li>""" % (li,entryDct['track']['artist']['name'], link, link,
                        entryDct['track']['album']['image'][3]['#text'],
                        entryDct['track']['album']['title'])
    return detail

# Creates the lightbox entry for each song. This will
# tell the user the name of the song, as well as the total number
# of listeners and plays, and its album.
def writeEntry(entryDct,link):
    entry = \
        """
        <li id=%s>
            	<div>
	            <h3>%s - <i>%s</i></h3>
		    <p>%s people have listened to this song, which has been played %s times.</p>
                    <p>You can get this song on the album %s, by %s.</p>
                    <a href="#" class="close">x</a>
            	</div>
            </li>""" %(link,entryDct['track']['artist']['name'], entryDct['track']['name'],
            entryDct['track']['listeners'], entryDct['track']['playcount'], 
           entryDct['track']['album']['title'], entryDct['track']['album']['artist'])
    return entry

# Compiles all of the HTML into one page by combining
# all of the data and earlier functions.
def writeHtmlPage(trackInfo, similarTracks):
# Write the start of the webpage's body.
    bodyStart = \
    """
    <body>

    <div id="container">
    <!--[if lte IE 8]>
    <noscript>
    <style>
    #information li { overflow: visible; position: relative; margin: 0 auto; margin-bottom: 25px; background: #fff; width: 600px; padding: 30px; height: auto; list-style: none; }	
    #information li div a.close { position: relative; background: transparent; padding: 0; color: #0090e2; font-size: 12px; font-weight: normal; left: 0; top: 0; }	
    iframe, .backface { display: none; }

    </style>
    </noscript>
    <![endif]-->

    <h2 class="title">Your Musical Tastes<span> according to %s</span></h2>

    <ul id="grid" class="group">
            """ %(trackInfo['track']['name'])

# Create the album grid for the main page, along with the lightbox page, for each song.
    detailList = writeDetails(trackInfo, formatParam(trackInfo['track']['name']),1)
    entryList =  writeEntry(trackInfo, formatParam(trackInfo['track']['name']))
    n = 2
    for song in similarTracks:
        fiName = song['name'] + "DetailedInfo.json"
        entryDct = json.load(open(fiName))
        link = formatParam(song['name'])
        detailList += writeDetails(entryDct, link, n)
        n = n+1
        entryList += writeEntry(entryDct, link)

# End the grid list and start the lightbox list.
    listTransition = \
    """
    </ul>
       
        <ul id="information">"""

# End the webpage.
    bodyEnd = \
    """
     </ul>

                <p style="text-align: center; margin-bottom: 50px;">Created by Caroline Gallagher. Design by <a href="http://tkenny.co.uk">Tom Kenny.</a> Data from <a href="http://last.fm"> <img src="lastfm_grey_small.gif" alt="last.fm"> </p>
    </body>
    </html>"""

# Putting all of the pieces of the webpage together and saving it.
    html = writeFirstPart(trackInfo['track']['name']) + bodyStart +\
           detailList + listTransition + entryList + bodyEnd
    title = formatParam(trackInfo['track']['name'])
    fiName = title + ".html"
    f = open(fiName, 'w')
    f.write(html)
    f.close()
    return fiName




     
