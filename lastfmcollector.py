#! /usr/bin/env python
# datacollection_updated.py
# Caroline Gallagher
# Written Feb 8, 2012
# Edited September 24, 2012 by Caroline Gallagher
# Edited September 9, 2013 to remove API key. You must register on the Last.FM website to obtain your own API key. It's free and easy.

import urllib2
import json
import os
from collections import defaultdict
import operator
import locale
from urllib import urlencode
from musicwebpagewriter import writeHtmlPage

prompt="Please enter the name of a song track."

URL = "http://ws.audioscrobbler.com/2.0/"

# Put your own API key here:
apikey = "7bad3906b79ea33eba804a92a31151df"

js = "&format=json"

# Formats the URL request and returns the data as a JSON object.
def jsonMaker (requestType, encodedInfo):
    request = URL + requestType + encodedInfo + "&api_key=" + apikey + js
    data = urllib2.urlopen(request).read()
    return json.loads(data)

# Takes in a track name from the user, and uses the last.fm database
# to find the best match. Returns the track name and artist for the best match.
def trackList(track):
    encodedTrack = urlencode({'track': track})
    dataJson = jsonMaker("?method=track.search&", encodedTrack)
    bestResult = [dataJson['results']['trackmatches']['track'][0]['name'],
                  dataJson['results']['trackmatches']['track'][0]['artist']]
    return bestResult

# Finds detailed track info of the best result for the track specified by the user.
# Places the detailed info into a .json file
def getTrackInfo (bestResult):
    encodedFields = urlencode({'track': bestResult[0], 'artist': bestResult[1]})
    dataJson = jsonMaker("?method=track.getinfo&", encodedFields)
    fiName = bestResult[0] + "DetailedInfo.json"
    f = open(fiName, 'w')
    json.dump(dataJson, f)
    f.close()

# Finds similar tracks to the track provided by the user that fit into certain parameters,
# and returns those tracks in a list of dictionaries. Each dictionary has the information
# for 1 similar track.
def getSimilarTracks (bestResult):
    encodedFields = urlencode({'track': bestResult[0], 'artist': bestResult[1]})
    dataJson = jsonMaker("?method=track.getsimilar&", encodedFields)
    uniqueArtist = [bestResult[1]]
    j = 0
    similarTracks = []

# While loop ends after 5 unique artists with album imagery have been identified
    while len (uniqueArtist) < 6:
        match = [u for u in uniqueArtist if u == dataJson['similartracks']['track'][j]['artist']['name']]
        if 'image' in dataJson['similartracks']['track'][j] and match == []:
                uniqueArtist.append(dataJson['similartracks']['track'][j]['artist']['name'])
                similarTracks.append(dataJson['similartracks']['track'][j])
        j = j + 1;
        
    fiName = bestResult[0] + "SimilarTracks.json" 
    f = open(fiName, 'w')
    json.dump(similarTracks, f)
    f.close()
    return similarTracks

# Get detailed page info for each of the similar tracks by invoking the
# getTrackInfo method
def getInfoSimilarTracks (similarTracks):
    for sim in similarTracks:
        result = []
        result.append(sim['name'])
        result.append(sim['artist']['name'])
        getTrackInfo(result)

# Prompts the user for a song, then finds the song, gets the song's detailed info,
# and finds similar tracks to the song. Also creates HTML files for the song
# and similar tracks.
def main():
    if apikey == "":
        print "You need to register for an API key at www.last.fm/api!"
        return
    print prompt
    track = raw_input("Song title: ")
    bestResult = trackList(track)
    getTrackInfo(bestResult)
    similarTracks = getSimilarTracks(bestResult)
    getInfoSimilarTracks(similarTracks)
    trackInfo = json.load(open(bestResult[0] + 'DetailedInfo.json'))
    simTracks = json.load(open(bestResult[0] + 'SimilarTracks.json'))
    pageName = writeHtmlPage(trackInfo, simTracks) 
    print "The webpage", pageName, "has been created"

# Execute the program in a terminal by typing ./lastfmcollector.py
if __name__ == "__main__":    
    main()
