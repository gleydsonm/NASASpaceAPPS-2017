#!/usr/bin/env python
'''
 * This is the TwitterGET module for #spaceapps software
 * Team Flash
 * Author: <gleydsonmazioli@gmail.com>
 *
 *
 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
'''
from BeautifulSoup import BeautifulSoup as soupy
import urllib
import re
import ssl
import socket
import sys
from config import *

# Maximum parset twitter args
MAX_PARSED_MSGS = 4


def connect_url(url):
    '''
    Connect to the remote host
    '''
    # Bypass SSL certificate validation (temporary workaround for lab)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        html = urllib.urlopen(url, context=ctx).read()
    except Exception,e:
        sys.exit("Connection failed with the remote host: "+str(e))
    soup = soupy(html)
    return soup


def parseexpressions(hit):
    '''
    Parse expressions trying to find Critical, Heavy and Light weather_word
    expressions in many different languages for correlations
    '''
    count = 1
    for l_lang in LANGS:
        # First analysys is done using Critical Weather conditions terms
        for weather_word in WEATHER_EXPRS_3[l_lang]:
            if weather_word+' ' in hit.contents[0].lower():
                if VERBOSE:
                    print 'CRITICAL Weather expression detected in %s language: %s in %s' % (l_lang, weather_word, hit.contents[0] )
                return { 'lang' : l_lang, 'level': 'CRITICAL', 'data': hit.contents[0]}

        # Second analysis id done using Heavy Weather condition terms
        for weather_word in WEATHER_EXPRS_2[l_lang]:
            if weather_word+' ' in hit.contents[0].lower():
                if VERBOSE:
                    print 'HEAVY Weather expression detected in %s language: %s in %s' % (l_lang, weather_word, hit.contents[0] )
                return { 'lang' : l_lang, 'level': 'HEAVY', 'data': hit.contents[0]}

        # Third analysis is done using light Weather condition terms
        for weather_word in WEATHER_EXPRS_1[l_lang]:
            if weather_word+' ' in hit.contents[0].lower():
                if VERBOSE:
                    print 'LIGHT Weather expression detected in %s language: %s in %s' % (l_lang, weather_word, hit.contents[0] )
                return { 'lang' : l_lang, 'level': 'LIGHT', 'data': hit.contents[0]}


def parsetweet(l_soup):
    '''
    Parse the Tweet message from the specified user. We also add
    auto-detection language based on ISO 3166 codes, and return them to the
    matrix of data to correlation. So we can also find out expressions about
    catastrophic events (Tsunamis, eartquares)
    '''
    count = 1
    for hit in l_soup.findAll("p", {"class":"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}):
        ret_list = parseexpressions(hit)
        count += 1
        if len(ret_list) > 0 or count > MAX_PARSED_MSGS:
            break
    return ret_list


def main():
    '''
    Main Twitter scan function
    '''
    soup = connect_url('https://twitter.com/gleydsonmazioli')
    tweets = parsetweet(soup)
    print tweets

if __name__ == '__main__':
    main()
