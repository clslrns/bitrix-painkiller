# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import re
import httplib, urllib
import json

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

    def get_component_signature( self, componentName ):
        conn = httplib.HTTPConnection('zitar.dev')
        conn.request( 'GET', '/bp.php?component=' + componentName )
        response = conn.getresponse()
        componentParams = json.loads( response.read() )
        conn.close()
        return componentParams

    def run( self, edit, block = False ):
        view = self.view
        path = view.file_name()

        for cursorId, cursorPos in enumerate( view.sel() ):
            name = self.find_name(view, cursorId)

            if not name:
                continue

            requestResult = self.get_component_signature( name )

            view.erase( edit, view.find( name, view.sel()[cursorId].begin() - len(name) ) )
            pref = ' ' * ( view.sel()[cursorId].begin() \
                           - view.line( view.sel()[cursorId].begin() ).begin() )

            print dir( requestResult )

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


