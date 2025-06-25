class KernFeatureWriter:
    """Skips generating the kern feature."""

    def __init__(self, font):
        pass

    def write(self, linesep="\n"):
        return ""
