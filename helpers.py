from time import gmtime, strftime
from PIL import Image, ExifTags

class PrtDecorator:
    last_output = None
def print_decorator(func):
    def wrapped_func(*args, **kwargs):
        prt = args[0]
        if PrtDecorator.last_output and len(prt) < len(PrtDecorator.last_output):
            prt = prt + (' ' * (len(PrtDecorator.last_output) - len(prt)))
            PrtDecorator.last_output = None
        for key, value in kwargs.items():
            if key == "end":
                PrtDecorator.last_output = prt

        return func(prt, '', **kwargs)
    return wrapped_func
    


def prttime():
    return strftime("%d/%m %H:%M", gmtime())




def adjustJPEGRotation(image):
    try:
        if hasattr(image, '_getexif'): # only present in JPEGs
            for orientation in ExifTags.TAGS.keys(): 
                if ExifTags.TAGS[orientation]=='Orientation':
                    break 
            e = image._getexif()       # returns None if no EXIF data
            if e is not None:
                exif=dict(e.items())
                orientation = exif[orientation] 

                if orientation == 3:   image = image.transpose(Image.ROTATE_180)
                elif orientation == 6: image = image.transpose(Image.ROTATE_270)
                elif orientation == 8: image = image.transpose(Image.ROTATE_90)
        return image
    except:
        return image