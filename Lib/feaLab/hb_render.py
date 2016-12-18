#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""hb_render.py

hb_render.HarfBuzzRenderer class 

wraps the 'hb-view' and 'hb-shape' Harfbuzz utilities
* https://github.com/behdad/harfbuzz
using the Python 'sh' module
* https://amoffat.github.io/sh/
* https://pypi.python.org/pypi/sh

"""

import json
import sys
import os.path
import warnings

try:
    from sh import hb_shape
except ImportError:
    warnings.warn("Run: brew install harfbuzz")
    warnings.warn("Run: pip install --user sh")
try:
    from sh import hb_view

    HB_VIEW = True
    """
    """
except ImportError:
    HB_VIEW = False

__version__ = "0.3"

class HarfBuzzRenderer(object):
    """Class to call the HarfBuzz `hb-view` or `hb-shape` tools via the `sh` module.

    Attributes:
        best_shaper (str):
            default HB shaper after hb.updateShapers(), otherwise 'ot'

        all_shapers (list):
            all available HB shapers after hb.updateShapers()

        os_shaper (str):
            default native platform HB shaper after hb.updateShapers()

        use_shapers (list):
            list of shapers for HB to try, used to call `hb-view` or `hb-shape`

        output_format (str):
            output format for `hb-view` / hb.toImage()
            can be 'svg' | 'png' | 'pdf' | 'ansi' | 'ps' | 'eps'
            default: 'svg'

        font_file (str):
            path to font file

        face_index (int):
            if font file is a TTC, the TTC sub-fontindex, otherwise 0

        font_size (int):
            the font size in pt to to use with `hb-shape` or `hb-view`
            default: 0 (means 'upem')

        text (unicode):
            input text as Unicode

        direction (str):
            text shaping direction
            can be: 'ltr' | 'rtl' | 'ttb' | 'btt' | 'auto'
            default: 'auto'

        script (str):
            ISO 15924 tag (not OpenType Script tag) for shaping, or 'auto'
            default: 'auto'

        language (str):
            ISO language tag (not OpenType LangSys tag) for shaping
            default: 'en'

        features (list):
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

            Example: hb.features=["aalt[3:5]=2","+kern","-liga"]

        bot (bool):
            Treat text as beginning_of_paragraph
        eot (bool):
            Treat text as end_of_paragraph
        text_before (unicode):
            Set text context before each line
        text_after (unicode):
            Set text context after each line
        preserve_default_ignorables (bool):
            Preserve Default_Ignorable characters, default: False
        utf8_clusters (bool):
            Use UTF8 byte indices, not char indices, default: False
        cluster_level (int):
            Cluster merging level: 0 | 1 | 2, default: 0
        normalize_glyphs (bool):
            Rearrange glyph clusters in nominal order
        num_iterations (int):
            Run shaper N times (default: 1)
        use_glyph_indexes (bool)
            Output glyph indices instead of names, like --no_glyph_names in `hb-*`
            default: False

        annotate (bool)
            Annotate output in hb.toImage()
            default: False
        background (str)
            Set background color '#rrggbb' | '#rrggbbaa' in hb.toImage()
            default: '#ffffff'
        foreground (str)
            Set foreground color '#rrggbb' | '#rrggbbaa' in hb.toImage()
            default: '#000000'
        line_space (int)
            add line gap between lines in units in hb.toImage()
            default: 0
        margin (list or int)
            Margin around output in hb.toImage()
            as one number or list of one to four numbers e.g. [16, 16, 16, 16]
            default: 16

    """
    def __init__(self, font_file=None, face_index=0, text=u''):
        """Initialize the HarfBuzzRenderer() object

        Args:
            font_file (str, optional): the path to the font file
            face_index (int, optional): the face index in a TTC file, 0 if non-TTC
            text (unicode, optional): Unicode text string to shape or render
        """
        self.best_shaper = 'ot'
        self.all_shapers = [self.best_shaper]
        self.os_shaper = self.best_shaper

        self.use_shapers = [self.best_shaper]

        self.font_file = font_file
        self.face_index = face_index
        self.font_size = 0

        self.text = text

        self.direction = 'auto'
        self.language = 'en'
        self.script = 'auto'
        self.features = []

        self.bot = False  #
        self.eot = False  #
        self.text_before = u''  #
        self.text_after = u''  #

        self.preserve_default_ignorables = False  #
        self.utf8_clusters = False  #
        self.cluster_level = 0  #
        self.normalize_glyphs = False  #
        self.num_iterations = 1  #
        self.use_glyph_indexes = False  # Output glyph indices instead of names

        self.annotate = False  # Annotate output toing
        self.background = '#ffffff'  # Set background color (rrggbb/rrggbbaa default: #FFFFFF)
        self.foreground = '#000000'  # Set foreground color (rrggbb/rrggbbaa, default: #000000)
        self.line_space = 0  # Set space between lines in units (default: 0)
        self.margin = [16, 16, 16, 16]  # Margin around output (one to four numbers , default: 16)

    def updateShapers(self):
        """Optional method to call `hb-shape`, get the list of HarfBuzz available
        shapers and assign them to self.all_shapers. Also populate self.best_shaper
        and self.os_shaper (the native platform shaper).

        Returns:
            None:
        """
        self.all_shapers = str(hb_shape(list_shapers=True)).splitlines()
        if sys.platform.startswith('win32'):
            if 'directwrite' in self.all_shapers and 'uniscribe' not in self.all_shapers:
                self.os_shaper = 'directwrite'
            elif 'uniscribe' in self.all_shapers:
                self.os_shaper = 'uniscribe'
        elif sys.platform.startswith('darwin'):
            if 'coretext' in self.all_shapers:
                self.os_shaper = 'coretext'
        if 'ot' not in self.all_shapers:
            self.best_shaper = self.os_shaper

    def openFont(self, font_file, face_index=0):
        """Convenience method to load a new font file

        Args:
            font_file (str):
            face_index (int, optional):
        """
        if os.path.exists(font_file):
            self.font_file = font_file
            self.face_index = face_index
        else:
            warnings.warn("Cannot open %s" % (font_file))
            self.font_file = None
            self.face_index = 0

    def _hb_shape(self, **kwargs):
        """Low-level method to call the `hb-shape` tool via the
        hb_shape virtual function provided by the `sh` module.

        Args:
            **kwargs (): passed from self.toJson()
                must be compatible with the `hb-shape` arguments
                where `--option-name=value` translates to option_name=value

        Returns:
            sh.RunningCommand:
        """
        return hb_shape(**kwargs)

    def _hb_view(self, **kwargs):
        """Low-level method to call the `hb-view` tool via the
        hb_view virtual function provided by the `sh` module.

        Args:
            **kwargs (): passed from self.toImage()
                must be compatible with the `hb-view` arguments
                where `--option-name=value` translates to option_name=value

        Returns:
            sh.RunningCommand:
        """
        return hb_view(**kwargs)

    def toJson(self, text=None):
        """Method to call hb_shape and get back the shaped JSON

        Args:
            text (unicode, optional): optional text, otherwise uses self.text

        Returns:
            None: if an error occurred
            list[dict, ...]: parsed JSON structure in `hb-shape` output format

        Example input:
            hb.toJson(text='Hello'))

        Example output:
            [
                {u'g': u'H', u'cl': 0, u'dx': 0, u'dy': 0, u'ay': 0, u'ax': 741},
                {u'g': u'e', u'cl': 1, u'dx': 0, u'dy': 0, u'ay': 0, u'ax': 421},
                {u'g': u'l', u'cl': 2, u'dx': 0, u'dy': 0, u'ay': 0, u'ax': 258},
                {u'g': u'l', u'cl': 3, u'dx': 0, u'dy': 0, u'ay': 0, u'ax': 253},
                {u'g': u'o', u'cl': 4, u'dx': 0, u'dy': 0, u'ay': 0, u'ax': 510}
            ]
        """
        text = text if text else self.text
        self.text = text
        hb_in = text.encode('utf-8')
        hb_out = self._hb_shape(
            _in=hb_in,
            _encoding="UTF-8",
            output_format='json',
            font_file=unicode(self.font_file).encode('utf-8'),
            face_index=self.face_index,
            font_size='upem' if self.font_size == 0 else self.font_size,
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
            shapers=",".join(self.use_shapers),
        )
        if hb_out.stderr:
            warnings.warn("`hb-view` returned an error: %s" % (hb_out.stderr))
            return None
        return json.loads(
            unicode(hb_out.stdout)
        )

    def _toImage(self, text=None, output_format='svg', font_size=None, output_file=False):
        """Method to call hb_view with the desired ouput format and get back:

        Args:
            text (unicode, optional): optional text, otherwise uses self.text
            output_format (str): 'svg' | 'png' | 'pdf' | 'ansi' | 'ps' | 'eps'
            font_size (int): the font size to use, 0 means 'upem', use self.font_size if omitted
            output_file (unicode): path to output_file, or False if stdout should be used

        Returns:
             None: if `hb-view` is not accessible or if an error occurs
             str: SVG (UTF-8), PNG or PDF buffer
             str: the output file path (UTF-8) if output_file was provided and the file was created
        """
        if not HB_VIEW:
            warnings.warn("`hb-view` not available")
            return None
        else:
            if font_size == 0:
                self.font_size = 0
                font_size = 'upem'
            elif font_size:
                font_size = font_size
                self.font_size = font_size
            else:
                font_size = self.font_size
            text = text if text else self.text
            self.text = text
            hb_in = unicode(text).encode('utf-8')
            hb_out = self._hb_view(
                _in=hb_in,
                _encoding="UTF-8",
                output_format=output_format,
                output_file=unicode(output_file).encode('utf-8') if output_file else False,
                font_file=unicode(self.font_file).encode('utf-8'),
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
                shapers=",".join(self.use_shapers),
                annotate=self.annotate,
                background=self.background,
                foreground=self.foreground,
                line_space=self.line_space,
                margin=self.margin if type(self.margin) == int else " ".join(str(i) for i in self.margin),
            )
            if hb_out.stderr:
                warnings.warn("`hb-view` returned an error: %s" % (hb_out.stderr))
                return None
            if output_file:
                output_path = os.path.realpath(output_file)
                if os.path.exists(output_path):
                    return output_path
                else:
                    warnings.warn("`hb-view` did not create file: %s" % (output_path))
                    return None
            else:
                return hb_out.stdout

    def toSVG(self, text=None, font_size=None, output_file=''):
        """

        Args:
            text (str):
            font_size (int):
            output_file (str):

        Returns:
            str:
                * empty string if an error occurred
                * SVG (UTF-8) content
                * the output file path (UTF-8) if output_file was provided and the file was created
        """
        data = self._toImage(text=text, font_size=font_size, output_file=output_file, output_format='svg')
        if data:
            return data
        else:
            return ''

    def toPNG(self, text=None, font_size=None, output_file=''):
        """

        Args:
            text (str):
            font_size (int):
            output_file (str):

        Returns:
            str:
                * empty string if an error occurred
                * PNG buffer
                * the output file path (UTF-8) if output_file was provided and the file was created
        """
        data = self._toImage(text=text, font_size=font_size, output_file=output_file, output_format='png')
        if data:
            return data
        else:
            return ''

    def toPDF(self, text=None, font_size=None, output_file=''):
        """

        Args:
            text (str):
            font_size (int):
            output_file (str):

        Returns:
            str:
                * empty string if an error occurred
                * PDF buffer
                * the output file path (UTF-8) if output_file was provided and the file was created
        """
        data = self._toImage(text=text, font_size=font_size, output_file=output_file, output_format='pdf')
        if data:
            return data
        else:
            return ''

def test():
    hb = HarfBuzzRenderer()
    hb.updateShapers()
    print(hb.all_shapers)
    hb.openFont('test/EBGaramond12-Regular.otf')
    text = u'Office staff'
    print(hb.toJson(text=text))
    hb.margin = 0
    hb.features = ['+dlig']
    size = 72
    print(hb.toSVG(text=text, font_size=size))
    print(hb.toSVG(text=text, font_size=size, output_file='test/EBGaramond12-Regular.svg'))
    print(hb.toPNG(text=text, font_size=size, output_file='test/EBGaramond12-Regular.png'))
    print(hb.toPDF(text=text, font_size=size, output_file='test/EBGaramond12-Regular.pdf'))
    help(hb)

if __name__ == '__main__':
    print('hb_render.py font_file [text] [font_size]')
    hb = HarfBuzzRenderer()
    hb.openFont(sys.argv[1] if len(sys.argv)>1 else u'test/EBGarąmońd12-Regular.otf')
    hb.text = unicode(sys.argv[2] if len(sys.argv) > 2 else u'O')
    hb.font_size = int(sys.argv[3] if len(sys.argv) > 3 else '20')
    print(hb.toSVG())
