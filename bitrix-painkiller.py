# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import re

class BitrixPainkillerCommand( sublime_plugin.TextCommand ):

    def find_name( self, view ):
        """Find name of bitrix component on the left from cursor."""
        end = view.sel()[0].end()
        if end < 3:
            return ''
        begin = end - 3

        lastMatch = ''
        while begin:
            regionContent = view.substr( sublime.Region( begin, end ) )
            # Component name match
            matchRes = re.match( '(\s|^)(([a-zA-Z_-]+):([a-zA-Z._-]+))', regionContent )
            if matchRes:
                lastMatch = matchRes.group(2)
            elif lastMatch or re.search( '\s', regionContent ):
                # Finish the iteration when we found one name 
                # or there is a space in search region
                begin = 1
            begin -= 1

        return lastMatch

    def get_component_signature( self, componentName ):
        pass

    def run( self, edit, block = False ):
        view = self.view
        path = view.file_name()

        print self.find_name(view)
