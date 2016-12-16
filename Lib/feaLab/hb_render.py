#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
hb_render.HarfBuzzRenderer class 

wraps the 'hb-view' and 'hb-shape' Harfbuzz utilities
* https://github.com/behdad/harfbuzz
using the Python 'sh' module
* https://amoffat.github.io/sh/
* https://pypi.python.org/pypi/sh

docs tbd, this is from hb-view docs:

    hb.features=["aalt[3:5]=2","+kern","-liga"]   

        Features can be enabled or disabled, either globally or limited to
        specific character ranges.  The format for specifying feature settings
        follows.  All valid CSS font-feature-settings values other than 'normal'
        and 'inherited' are also accepted, though, not documented below.

        The range indices refer to the positions between Unicode characters,
        unless the --utf8-clusters is provided, in which case range indices
        refer to UTF-8 byte indices. The position before the first character
        is always 0.

        The format is Python-esque.  Here is how it all works:

            Syntax:       Value:    Start:    End:

        Setting value:
            "kern"        1         0         ∞         # Turn feature on
            "+kern"       1         0         ∞         # Turn feature on
            "-kern"       0         0         ∞         # Turn feature off
            "kern=0"      0         0         ∞         # Turn feature off
            "kern=1"      1         0         ∞         # Turn feature on
            "aalt=2"      2         0         ∞         # Choose 2nd alternate

        Setting index:
            "kern[]"      1         0         ∞         # Turn feature on
            "kern[:]"     1         0         ∞         # Turn feature on
            "kern[5:]"    1         5         ∞         # Turn feature on, partial
            "kern[:5]"    1         0         5         # Turn feature on, partial
            "kern[3:5]"   1         3         5         # Turn feature on, range
            "kern[3]"     1         3         3+1       # Turn feature on, single char

        Mixing it all:

            "aalt[3:5]=2" 2         3         5         # Turn 2nd alternate on for range

            """

import sys
import json
import warnings
try: 
        from sh import hb_shape
except ImportError:
        warnings.warn("Run: brew install harfbuzz")
        warnings.warn("Run: pip install --user sh")
try: 
        from sh import hb_view
        HB_VIEW = True
except ImportError:
        HB_VIEW = False

class HarfBuzzRenderer(object): 
    def __init__(self, font_file = None, face_index = 0, text = u''): 
        self.shaper = 'ot'
        self.all_shapers = [self.shaper]
        self.shaper_os = self.shaper

        self.shapers = [self.shaper]             # Set comma_separated list of shapers to try

        self.font_file = font_file               # Set font file_name
        self.face_index = face_index             # Set face index (default: 0)
        self.font_size='upem'                    # Font size (default: upem)

        self.text=text                           # Set input text as Unicode
        self.text_file=None                      # path to text file (text file overrides text)

        self.direction='auto'                    # Set text direction: 'ltr'|'rtl'|'ttb'|'btt'|'auto'
        self.language='en'                       # Set text language ISO
        self.script='auto'                       # Set text script (ISO_15924 tag, default: auto)
        self.features=[]                         # list of font features e.g. ["aalt[3:5]=2","+kern","-liga"]

        self.bot=False                           # Treat text as beginning_of_paragraph
        self.eot=False                           # Treat text as end_of_paragraph
        self.text_before=u''                     # Set text context before each line
        self.text_after=u''                      # Set text context after each line

        self.preserve_default_ignorables=False   # Preserve Default_Ignorable characters
        self.utf8_clusters=False                 # Use UTF8 byte indices, not char indices
        self.cluster_level=0                     # Cluster merging level 0 | 1 | 2 (default: 0)
        self.normalize_glyphs=False              # Rearrange glyph clusters in nominal order
        self.num_iterations=1                    # Run shaper N times (default: 1)
        self.use_glyph_indexes=False             # Output glyph indices instead of names

        self.annotate=False                      # Annotate output toing
        self.background='#ffffff'                # Set background color (rrggbb/rrggbbaa default: #FFFFFF)
        self.foreground='#000000'                # Set foreground color (rrggbb/rrggbbaa, default: #000000)
        self.line_space=0                        # Set space between lines in units (default: 0)
        self.margin=[16, 16, 16, 16]             # Margin around output (one to four numbers , default: 16)

    def updateShapers(self): 
        self.all_shapers = str(hb_shape(list_shapers=True)).splitlines()
        if sys.platform.startswith('win32'):
            if 'directwrite' in self.all_shapers and 'uniscribe' not in self.all_shapers:
                self.shaper_os = 'directwrite'
            elif 'uniscribe' in self.all_shapers:
                self.shaper_os = 'uniscribe'
        elif sys.platform.startswith('darwin'):    
            if 'coretext' in self.all_shapers:
                self.shaper_os = 'coretext'
        if 'ot' not in self.all_shapers: 
            self.shaper = self.shaper_os

    def loadFont(self, font_file, face_index=0):
        self.font_file = font_file
        self.face_index = face_index

    def toJson(self, text=None):
        text = text if text else self.text
        self.text = text
        hb_in = text.encode('utf-8')
        hb_out = hb_shape(
            _in=hb_in,
            output_format='json',
            font_file=self.font_file, 
            face_index=self.face_index, 
            font_size=self.font_size, 
            show_text=False,
            show_unicode=False,
            show_extents=False,
            language=self.language,
            direction=self.direction, 
            script=self.script, 
            features=",".join(self.features), 
            bot=self.bot, 
            eot=self.eot, 
            text_before=self.text_before,
            text_after=self.text_after,
            preserve_default_ignorables=self.preserve_default_ignorables,
            utf8_clusters=self.utf8_clusters,
            cluster_level=self.cluster_level,
            normalize_glyphs=self.normalize_glyphs,
            num_iterations=self.num_iterations,
            no_glyph_names=self.use_glyph_indexes,
            shapers=",".join(self.shapers),
        )
        return json.loads(
            unicode(hb_out)
            )

    def toImage(self, text=None, format='svg', font_size=None, output_file=False): 
        if not HB_VIEW:
            return None
        else:  
            font_size = font_size if font_size else self.font_size
            self.font_size = font_size
            text = text if text else self.text
            self.text = text
            hb_in = text.encode('utf-8')
            hb_out = hb_view(
                _in=hb_in,
                output_format=format,
                output_file=output_file, 
                font_file=self.font_file, 
                face_index=self.face_index, 
                font_size=font_size, 
                show_text=False,
                show_unicode=False,
                show_extents=False,
                language=self.language,
                direction=self.direction, 
                script=self.script, 
                features=",".join(self.features), 
                bot=self.bot, 
                eot=self.eot, 
                text_before=self.text_before,
                text_after=self.text_after,
                preserve_default_ignorables=self.preserve_default_ignorables,
                utf8_clusters=self.utf8_clusters,
                cluster_level=self.cluster_level,
                normalize_glyphs=self.normalize_glyphs,
                num_iterations=self.num_iterations,
                no_glyph_names=self.use_glyph_indexes,
                shapers=",".join(self.shapers),
                annotate=self.annotate,
                background=self.background,
                foreground=self.foreground,
                line_space=self.line_space,
                margin=self.margin if type(self.margin) == int else " ".join(self.margin),
            )
            if output_file: 
                return output_file
            else: 
                return hb_out

    def toSVG(self, text=None, font_size=None, output_file=False): 
        return self.toImage(text=text, font_size=font_size, output_file=output_file, format='svg')

    def toPNG(self, text=None, font_size=None, output_file=False): 
        return self.toImage(text=text, font_size=font_size, output_file=output_file, format='png')

    def toPDF(self, text=None, font_size=None, output_file=False): 
        return self.toImage(text=text, font_size=font_size, output_file=output_file, format='pdf')

if __name__ == '__main__':
    hb = HarfBuzzRenderer()
    hb.updateShapers()
    print(hb.all_shapers)
    hb.font_file = 'test/MinionPro-Regular.otf'
    print(hb.toJson(text='Hello'))
    hb.margin=0
    print(hb.toSVG(text='Hello', font_size=23))
    print(hb.toPNG(text='Hello', font_size=23, output_file='test.png'))
    print(hb.toPDF(text='Hello', font_size=23, output_file='test.pdf'))
