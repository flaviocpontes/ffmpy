__author__ = 'flaviopontes'

class _DataPads:

    def __init__(self):
        self.data_type = None
        self.media_stream = None


class VideoDataPad(_DataPads):

    def __init__(self):
        self.data_type = 'video'


class AudioDataPad(_DataPads):

    def __init__(self):
        self.data_type = 'video'


class _InputNode:

    def __init__(self, media_file=None, template=None):
        pass

