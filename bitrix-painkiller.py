# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import re

class BitrixPainkillerCommand( sublime_plugin.TextCommand ):

    def find_name( self, view ):
        """Find name of bitrix component on the left from cursor."""
        end = view.sel()[0].end()
        
        regionContent = view.substr( sublime.Region( 0, end ) )
        matchRes = re.match( '(^|\s)(([a-zA-Z_-]+):([a-zA-Z._-]+))', regionContent )
        return matchRes.group(2)

    def get_component_signature( self, componentName ):
        pass

    def run( self, edit, block = False ):
        view = self.view
        path = view.file_name()

        print self.find_name(view)
