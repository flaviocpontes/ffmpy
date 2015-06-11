# -*- coding: utf-8 -*-

from ffmpy import __author__, __version__, __version_info__, __copyright__

video_codecs = {'mpeg2video': 'MPEG-2 video',
                'h264': 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10',
                'vp8': 'On2 VP8',
                'mpeg4': 'MPEG-4 part 2',
                'theora': 'Theora',
                'msmpeg4v2': 'MPEG-4 part 2 Microsoft variant version 2',
                'vc1': 'SMPTE VC-1',
                'mjpeg': 'MJPEG (Motion JPEG)'}

audio_codecs = {'flac': 'FLAC (Free Lossless Audio Codec)',
                'mp3': 'MP3 (MPEG audio layer 3)',
                'vorbis': 'Vorbis',
                'aac': 'AAC (Advanced Audio Coding)',
                'mp2': 'MP2 (MPEG audio layer 2)',
                'pcm_s16le': 'PCM signed 16-bit little-endian',
                'wmav2': 'Windows Media Audio 2'}

image_codecs = {'png': 'PNG (Portable Network Graphics) image',
                'bmp': 'BMP (Windows and OS/2 bitmap)',
                'gif': 'GIF (Graphics Interchange Format)',
                'alias_pix': 'Alias/Wavefront PIX image',
                'pgm': 'PGM (Portable GrayMap) image',
                'tiff': 'TIFF image',
                'targa': 'Truevision Targa image',
                }

subtitle_codecs = {'ass': 'ASS (Advanced SubStation Alpha) subtitle',
                   'subrip': 'SubRip subtitle',
                   'hdmv_pgs_subtitle': 'HDMV Presentation Graphic Stream subtitles',
                   'pgssub': 'HDMV Presentation Graphic Stream subtitles'}

video_formats = {'mov,mp4,m4a,3gp,3g2,mj2': 'QuickTime / MOV',
                 'matroska,webm': 'Matroska / WebM',
                 'avi': 'AVI (Audio Video Interleaved)',
                 'ogg': 'Ogg',
                 'asf': 'ASF (Advanced / Active Streaming Format)',
                 'mxf': 'MXF (Material eXchange Format)'}

audio_formats = {'flac': 'raw FLAC',
                 'mp3': 'MP2/3 (MPEG audio layer 2/3)',
                 'ogg': 'Ogg'}

image_formats = {'png_pipe': 'piped png sequence',
                 'bmp_pipe': 'piped bmp sequence',
                 'gif': 'CompuServe Graphics Interchange Format (GIF)',
                 'alias_pix': 'Alias/Wavefront PIX image',
                 'tiff_pipe': 'piped tiff sequence',
                 'mpeg': 'MPEG-PS (MPEG-2 Program Stream)',
                 'image2': 'image2 sequence'}

def get_codec_long_name(codec_name):
    conversion_table = dict(list(video_codecs.items()) +
                            list(audio_codecs.items()) +
                            list(image_codecs.items()) +
                            list(subtitle_codecs.items()))

    return conversion_table.get(codec_name, '')


def get_format_long_name(format_name):
    conversion_table = dict(list(video_formats.items()) +
                            list(audio_formats.items()) +
                            list(image_formats.items()))
    return conversion_table.get(format_name, '')

