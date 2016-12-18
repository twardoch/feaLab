Module feaLab.hb_render
-----------------------

Variables
---------
HB_VIEW

Functions
---------
main()

test()

Classes
-------
HarfBuzzRenderer 
    Class to call the HarfBuzz `hb-view` or `hb-shape` tools via the `sh` module.

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
                "kern"        1         0         $         # Turn feature on
                "+kern"       1         0         $         # Turn feature on
                "-kern"       0         0         $         # Turn feature off
                "kern=0"      0         0         $         # Turn feature off
                "kern=1"      1         0         $         # Turn feature on
                "aalt=2"      2         0         $         # Choose 2nd alternate

            Setting index:
                "kern[]"      1         0         $         # Turn feature on
                "kern[:]"     1         0         $         # Turn feature on
                "kern[5:]"    1         5         $         # Turn feature on, partial
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

    Ancestors (in MRO)
    ------------------
    feaLab.hb_render.HarfBuzzRenderer
    __builtin__.object

    Instance variables
    ------------------
    all_shapers

    annotate

    background

    best_shaper

    bot

    cluster_level

    direction

    eot

    face_index

    features

    font_file

    font_size

    foreground

    language

    line_space

    margin

    normalize_glyphs

    num_iterations

    os_shaper

    preserve_default_ignorables

    script

    text

    text_after

    text_before

    use_glyph_indexes

    use_shapers

    utf8_clusters

    Methods
    -------
    __init__(self, font_file=None, face_index=0, text=u'')
        Initialize the HarfBuzzRenderer() object

        Args:
            font_file (str, optional): the path to the font file
            face_index (int, optional): the face index in a TTC file, 0 if non-TTC
            text (unicode, optional): Unicode text string to shape or render

    openFont(self, font_file, face_index=0)
        Convenience method to load a new font file

        Args:
            font_file (str):
            face_index (int, optional):

    toJson(self, text=None)
        Method to call hb_shape and get back the shaped JSON

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

    toPDF(self, text=None, font_size=None, output_file='')
        Args:
            text (str):
            font_size (int):
            output_file (str):

        Returns:
            str:
                * empty string if an error occurred
                * PDF buffer
                * the output file path (UTF-8) if output_file was provided and the file was created

    toPNG(self, text=None, font_size=None, output_file='')
        Args:
            text (str):
            font_size (int):
            output_file (str):

        Returns:
            str:
                * empty string if an error occurred
                * PNG buffer
                * the output file path (UTF-8) if output_file was provided and the file was created

    toSVG(self, text=None, font_size=None, output_file='')
        Args:
            text (str):
            font_size (int):
            output_file (str):

        Returns:
            str:
                * empty string if an error occurred
                * SVG (UTF-8) content
                * the output file path (UTF-8) if output_file was provided and the file was created

    updateShapers(self)
        Optional method to call `hb-shape`, get the list of HarfBuzz available
        shapers and assign them to self.all_shapers. Also populate self.best_shaper
        and self.os_shaper (the native platform shaper).

        Returns:
            None:
