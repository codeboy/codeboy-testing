from imagekit.specs import ImageSpec
from imagekit import processors




# First we define our "processors". ImageKit ships with four configurable
# processors: Adjustment, Resize, Reflection and Transpose. You can also
# create your own processors. Processors are configured by subclassing and
# overriding specific class variables.

class ResizeThumbnail(processors.Resize):
    width = 120
    height = 100
    crop = True

class ResizeRegion(processors.Resize):
    width = 90
    height = 90
    crop = True

class ResizeAdv(processors.Resize):
    width = 218
    height = 69
    crop = True

class ResizeAvatar(processors.Resize):
    width = 90
    height = 120
    crop = True

class ResizeDisplay(processors.Resize):
    width = 600

class EnhanceSmall(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1

# Next we define our specifications or "specs". Image specs are where we define
# the individual "classes" of images we want to have access to. Like processors
# image specs are configured by subclasses the ImageSpec superclass.

class AdminThumbnail(ImageSpec):
    access_as = 'admin_thumbnail'
    processors = [ResizeThumbnail, EnhanceSmall]


class Display(ImageSpec):
    increment_count = True
    processors = [ResizeDisplay]


class Thumbnail(ImageSpec):
    processors = [ResizeThumbnail, EnhanceSmall]
    pre_cache = True


class Avatar(ImageSpec):
    processors = [ResizeAvatar, EnhanceSmall]
    pre_cache = True


class Region(ImageSpec):
    processors = [ResizeRegion, EnhanceSmall]
    pre_cache = True


class Adv(ImageSpec):
    processors = [ResizeAdv, EnhanceSmall]
    pre_cache = True
