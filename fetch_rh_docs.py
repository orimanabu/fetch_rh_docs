#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import requests
import subprocess
from argparse import ArgumentParser
from getpass import getpass
from lxml import html
from pprint import pprint
import keyring

top_url = 'https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/'
top_url = 'https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/'

def fetch_top_page(session, url):
    res = session.get(url)
    return res.content

def parse_pdf_urls(content, filters):
    tree = html.fromstring(content)
    urls = [elem.attrib['href'].strip().replace('/site', 'https://access.redhat.com') for elem in tree.xpath('//a[.="PDF"]')]
    if filters:
        for f in filters:
            ro = re.compile(f)
            urls = [url for url in urls if ro.search(url)]
    return urls

def parse_kb_urls(content, filters):
    tree = html.fromstring(content)
    urls = [elem.attrib['href'].strip() for elem in tree.xpath('//a[@class="external"]')]
    if filters:
        for f in filters:
            ro = re.compile(f)
            urls = [url for url in urls if ro.search(url)]
    return urls

def fetch_kb_content(session, url, username, password):
    res = session.get(url)
    #print "*", res.url
    tree = html.fromstring(res.content)
    login_elem = tree.xpath('//div[@class="messages warning entitlement-message"]')
    if not login_elem:
        return tree.xpath('//title')[0].text, res.content
    login_url = [elem.attrib['href'] for elem in login_elem[0].xpath('./*/a') if 'login' in elem.attrib['href']][0]
    print '  login_url:', login_url

    res = session.get(login_url)
    #print "###1"
    #print "*", res.url
    #print res.content
    tree = html.fromstring(res.content)
    action = tree.xpath('//form')[0].attrib['action']
    data = dict([(elem.attrib['name'], elem.attrib['value']) for elem in tree.xpath('//form')[0].xpath('./input')])

    res = session.post(action, data=data)
    #print "###2"
    #print "*", res.url
    #print res.content
    tree = html.fromstring(res.content)
    action = res.url + tree.xpath('//form[@id="login_form"]')[0].attrib['action']
    data = dict([(elem.attrib['name'], elem.attrib['value']) for elem in tree.xpath('//form[@id="login_form"]')[0].xpath('./*/*/input')])

    print "** This page requires RHN login."
    if not username:
        username = raw_input('    username: ')
    if not password:
        password = keyring.get_password('fetch_rhn_docs', username)
        if not password:
            password = getpass('    password: ')
            keyring.set_password('fetch_rhn_docs', username, password)

    data['j_username'] = username
    data['j_password'] = password
    res = session.post(action, data=data)
    #print "###3"
    #print "*", res.url
    #print res.content
    tree = html.fromstring(res.content)
    action = tree.xpath('//form')[0].attrib['action']
    data = dict([(elem.attrib['name'], elem.attrib['value']) for elem in tree.xpath('//form')[0].xpath('./input')])

    res = session.post(action, data=data)
    #print "###4"
    #print "*", res.url
    #print res.content
    tree = html.fromstring(res.content)
    return tree.xpath('//title')[0].text, res.content

def parse_args():
    desc = u'''{0} [Args] [Options]
Detailed options -h or --help'''.format(__file__)
    parser = ArgumentParser(description=desc)
    parser.add_argument('-u', '--username', type=str, dest='username', help='RHN username')
    parser.add_argument('-P', '--password', type=str, dest='password', help='RHN password')
    parser.add_argument('-l', '--list', action='store_true', dest='list_only', help='only print list of urls.')
    parser.add_argument('-p', '--pdf', action='store_true', dest='pdf', help='download pdf files')
    #parser.add_argument('-e', '--epub', action='store_true', dest='epub', help='download epub files')
    #parser.add_argument('-S', '--single-html', action='store_true', dest='single_html', help='download single html files')
    parser.add_argument('-k', '--kb', action='store_true', dest='kb', help='download kb')
    parser.add_argument('-c', '--convert-to-pdf', action='store_true', dest='convert_to_pdf', help='convert html to pdf')
    parser.add_argument('-f', '--filter', action='append', dest='filter', help='regexp to filter url.')
    parser.add_argument('url', nargs='?')
    args = parser.parse_args()
    if args.url is None:
        args.url = top_url
    print "(debug) %s: %s" % ('username', args.username)
    print "(debug) %s: %s" % ('password', args.password)
    print "(debug) %s: %s" % ('list', args.list_only)
    print "(debug) %s: %s" % ('pdf', args.pdf)
    #print "(debug) %s: %s" % ('epub', args.epub)
    #print "(debug) %s: %s" % ('single_html', args.single_html)
    print "(debug) %s: %s" % ('kb', args.kb)
    print "(debug) %s: %s" % ('convert_to_pdf', args.convert_to_pdf)
    print "(debug) %s: %s" % ('filter', args.filter)
    print "(debug) %s: %s" % ('url', args.url)
    return args

def main():
    args = parse_args()
    session = requests.Session()
    content = fetch_top_page(session, args.url)
    #print content

    if args.pdf:
        print "# pdf"
        for url in parse_pdf_urls(content, args.filter):
            print url
            if args.list_only:
                continue
            print "  * Downloading..."
            cmd = "/usr/bin/curl -O '%s' > /dev/null 2>&1" % url
            #print "      ", cmd
            subprocess.call(cmd, shell=True)

    if args.kb:
        print "# kb"
        for url in parse_kb_urls(content, args.filter):
            print url
            if args.list_only:
                continue
            title, content = fetch_kb_content(session, url, args.username, args.password)
            print "  title:", title
            print "  * Downloading..."
            f = open(title + '.html', 'w')
            f.write(content)
            f.close()
            if args.convert_to_pdf:
                print "  * Converting to pdf..."
                cmd = "/usr/local/bin/wkhtmltopdf --load-error-handling ignore --load-media-error-handling ignore --disable-external-links '%s' '%s' > /dev/null 2>&1" % (title + '.html', title + '.pdf')
                #subprocess.call(cmd.strip().split(" "))
                #print "      ", cmd
                subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    main()
