# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import re
import httplib, urllib
import json
import os

__version__      = '0.1'
__core_version__ = '0.1'
__authors__      = ['"Vitaly Chirkov" <vitaly.chirkov@gmail.com>']

# load settings
settings = sublime.load_settings('Painkiller.sublime-settings')

class BitrixPainkillerCommand( sublime_plugin.TextCommand ):

    def find_name( self, view, cursorId ):
        """Find name of Bitrix component on the left from cursor."""
        end = view.sel()[cursorId].end()

        regionContent = view.substr( view.line( end ) )

        matchRes = re.search( \
            '(?P<cname>([a-zA-Z_-]+):([a-zA-Z._-]+))', \
            regionContent \
        )
        return matchRes.group('cname') if matchRes else None

    def file_get_contents( self, filename ):
        """ http://stackoverflow.com/questions/1432126/how-to-get-content-of-a-small-ascii-file-in-python"""
        with open(filename) as f:
            return f.read()

    def get_host( self, filepath ):
        """ Find hostname file and get host for any file in webroot directory."""
        pathChunks = filepath.split( '/bitrix/' )

        if len( pathChunks ) > 1:
            # Найдена директория bitrix
            # Проверим, есть ли в ней наш модуль
            pathChunks.pop()
            currentPath = ''
            for chunk in pathChunks:
                currentPath += chunk + '/bitrix/'
                filename = currentPath + 'modules/thelikers.painkiller/site_host'
                if( os.path.exists( filename ) ):
                    host = self.file_get_contents( filename )
                    if( host ):
                        return host

        pathChunks = filepath.split('/')
        pathChunks.pop()

        currentPath = ''
        for chunk in pathChunks:
            currentPath += chunk + '/'

            filename = currentPath + 'bitrix/modules/thelikers.painkiller/site_host'
            if( os.path.exists( filename ) ):
                host = self.file_get_contents( filename )
                if( host ):
                    return host

        return false

    def get_component_signature( self, componentName, host ):
        conn = httplib.HTTPConnection( host )
        conn.request( 'GET', '/bitrix/tools/painkiller_component_signature.php?component=' + componentName )
        response = conn.getresponse()
        componentParams = json.loads( response.read() )
        conn.close()
        return componentParams

    def run( self, edit, block = False ):
        view = self.view
        path = view.file_name()
        host = self.get_host( path )

        if not host:
            return false

        for cursorId, cursorPos in enumerate( view.sel() ):
            name = self.find_name(view, cursorId)

            if not name:
                continue

            requestResult = self.get_component_signature( name, host )

            view.erase( edit, view.find( name, view.sel()[cursorId].begin() - len(name) ) )
            pref = ' ' * ( view.sel()[cursorId].begin() \
                           - view.line( view.sel()[cursorId].begin() ).begin() )

            params = u''
            if requestResult['status'] == 'found':
                for key in requestResult['data']:
                    params += "%s        '%s' => '%s',\n" % (pref, key, requestResult['data'][key])

            code = "<?$APPLICATION->IncludeComponent(\n" \
                 + "{pref}    '{name}',\n" \
                 + "{pref}    '',\n" \
                 + "{pref}    array(\n{params}" \
                 + "{pref}    )\n" \
                 + "{pref})?>"
            code = code.format( pref = pref, name = name, params = params )

            view.insert(edit, view.sel()[cursorId].end(), code)


