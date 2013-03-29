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
        if self.host:
            try:
                self.conn = httplib.HTTPConnection( self.host )
                params = urllib.urlencode({'component': self.componentName})
                self.conn.request( 'GET', self.apiUrl + '?' + params  )
                response = self.conn.getresponse()
                self.result = json.loads( response.read() )
                self.conn.close()
            except socket.error:
                self.result = { 'status': 'network_error' }
        else:
            self.result = { 'status': 'no_host' }

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
        try:
            pathChunks = filepath.split( os.sep )
        except AttributeError:
            return False

        pathChunks.pop()

        currentPath = ''
        for chunk in pathChunks:
            currentPath += chunk + os.sep
            filename = currentPath \
                     + 'bitrix' + os.sep \
                     + 'modules' + os.sep \
                     + 'thelikers.painkiller' + os.sep \
                     + 'site_host'
            if os.path.exists( filename ):
                host = self.file_get_contents( filename )
                if host:
                    return host

        return False

    def replace( self, name, selId, reqResult ):
        """ Replaces component name by generated code, based on recieved component' params"""
        view = self.view
        settings = view.settings()
        edit = view.begin_edit('bitrix-painkiller')
        view.erase( edit, view.find( name, view.sel()[selId].begin() - len(name) ) )

        # Margin for generated lines equals current line' left margin
        margin = view.sel()[selId].begin() - view.line( view.sel()[selId].begin() ).begin()

        prefUnit = ' ' * settings.get('tab_size') if settings.get('translate_tabs_to_spaces') else '\t'
        pref = ' ' * margin if settings.get('translate_tabs_to_spaces') else '\t'

        params = u''
        if reqResult['status'] == 'found':
            for key in reqResult['data']:
                param = "{pref}{pu}{pu}'{key}' => '{val}',\n"
                params += param.format( pref = pref, key = key, val = reqResult['data'][key], pu = prefUnit )

        code = "<?$APPLICATION->IncludeComponent(\n" \
             + "{pref}{pu}'{name}',\n" \
             + "{pref}{pu}'',\n" \
             + "{pref}{pu}array(\n{params}" \
             + "{pref}{pu})\n" \
             + "{pref})?>"
        code = code.format( pref = pref, name = name, params = params, pu = prefUnit )

        view.insert( edit, view.sel()[selId].end(), code )
        view.end_edit(edit)

    def run( self, edit ):
        view = self.view
        path = view.file_name()
        host = self.get_host( path )

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
