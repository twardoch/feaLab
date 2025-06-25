class MarkFeatureWriter:
    """Skips generating the mark and mkmk features."""

    def __init__(self, font, anchorList=(), mkmkAnchorList=(), ligaAnchorList=()):
        pass

    def write(self, doMark=False, doMkmk=False):
        return ""
