# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import re
import httplib, urllib
import json
import os
import socket
import threading

__version__      = '0.1'
__core_version__ = '0.1'
__authors__      = ['"Vitaly Chirkov" <vitaly.chirkov@gmail.com>']

# load settings
settings = sublime.load_settings('Painkiller.sublime-settings')

class BitrixPainkillerApiCall( threading.Thread ):
    """ Asynchronous call for Bitrix module API"""
    def __init__( self, componentName, host, selId, timeout ):
        self.componentName = componentName
        self.host = host
        self.selId = selId
        self.timeout = timeout
        self.result = None
        self.conn = None
        self.apiUrl = '/bitrix/tools/painkiller_component_signature.php'
        threading.Thread.__init__(self)

    def stop(self):
        if( self.conn ):
            self.conn.close()
        self._Thread__stop()

    def run(self):
        """ Send requests for component default parameters to site script"""
        try:
            self.conn = httplib.HTTPConnection( self.host )
            params = urllib.urlencode({'component': self.componentName})
            self.conn.request( 'GET', self.apiUrl + '?' + params  )
            response = self.conn.getresponse()
            self.result = json.loads( response.read() )
            self.conn.close()
        except socket.error:
            self.result = { 'status': 'network_error' }

class BitrixPainkillerCommand( sublime_plugin.TextCommand ):

    threads = []

    def find_name( self, view, selId ):
        """Find name of Bitrix component on the left from cursor"""
        end = view.sel()[selId].end()

        regionContent = view.substr( view.line( end ) )

        matchRes = re.search(
            '(?P<cname>([a-zA-Z_-]+):([a-zA-Z._-]+))',
            regionContent
        )
        return matchRes.group('cname') if matchRes else None

    def file_get_contents( self, filename ):
        """ http://stackoverflow.com/questions/1432126/how-to-get-content-of-a-small-ascii-file-in-python"""
        with open(filename) as f:
            return f.read()

    def get_host( self, filepath ):
        """ Find hostname file and get host for any file in webroot directory"""
        pathChunks = filepath.split( '/bitrix/' )

        if len( pathChunks ) > 1:
            # Bitrix directory found
            # Check if our module exists in it
            pathChunks.pop()
            currentPath = ''
            for chunk in pathChunks:
                currentPath += chunk + '/bitrix/'
                filename = currentPath + 'modules/thelikers.painkiller/site_host'
                if os.path.exists( filename ):
                    host = self.file_get_contents( filename )
                    if( host ):
                        return host

        pathChunks = filepath.split('/')
        pathChunks.pop()

        currentPath = ''
        for chunk in pathChunks:
            currentPath += chunk + '/'

            filename = currentPath + 'bitrix/modules/thelikers.painkiller/site_host'
            if os.path.exists( filename ):
                host = self.file_get_contents( filename )
                if( host ):
                    return host

        return False

    def replace( self, name, selId, reqResult ):
        """ Replaces component name by generated code, based on recieved component' params"""

        print 'thread ' + name

        view = self.view
        edit = view.begin_edit('bitrix-painkiller')
        view.erase( edit, view.find( name, view.sel()[selId].begin() - len(name) ) )

        # Left margin for generated lines equals current line' left margin
        pref = ' ' * ( view.sel()[selId].begin()
                       - view.line( view.sel()[selId].begin() ).begin() )

        params = u''
        if reqResult['status'] == 'found':
            for key in reqResult['data']:
                params += "%s        '%s' => '%s',\n" % (pref, key, reqResult['data'][key])

        code = "<?$APPLICATION->IncludeComponent(\n" \
             + "{pref}    '{name}',\n" \
             + "{pref}    '',\n" \
             + "{pref}    array(\n{params}" \
             + "{pref}    )\n" \
             + "{pref})?>"
        code = code.format( pref = pref, name = name, params = params )

        view.insert( edit, view.sel()[selId].end(), code )
        view.end_edit(edit)

    def run( self, edit ):
        view = self.view
        path = view.file_name()
        host = self.get_host( path )

        if not host:
            return False

        for thread in self.threads:
            thread.stop()

        self.threads = []
        for selId, cursorPos in enumerate( view.sel() ):
            name = self.find_name(view, selId)
            if not name:
                continue

            thread = BitrixPainkillerApiCall( name, host, selId, 5 )
            self.threads.append(thread)
            thread.start()

        self.handle_threads()

    def handle_threads(self):
        next_threads = []
        for thread in self.threads:
            if thread.is_alive():
                next_threads.append(thread)
                continue
            offset = self.replace( thread.componentName, thread.selId, thread.result )
        self.threads = next_threads

        if len(self.threads):
            sublime.set_timeout( self.handle_threads, 100 )
