import re
from unicodedata import normalize, decomposition
from plone.i18n.normalizer.base import allowed, mapping
from plone.i18n.normalizer import cropName, baseNormalize
from plone.i18n.normalizer import NON_WORD_REGEX
from plone.i18n.normalizer import MULTIPLE_DASHES_REGEX, EXTRA_DASHES_REGEX

IGNORE_REGEX = re.compile(r"['\"()]")

mapping.update({
    305 : 'i',
    })

class BAtlasNormalizer(object):
    """
    This normalizer can normalize any unicode string and returns a
    version that only contains of ASCII characters allowed in a typical
    scripting or programming language id, such as CSS class names or Python
    variable names for example.
    """

    def normalizeN(self, label):
        """Returns a normalized text. text has to be a unicode string.
        """
        for text in label.split('/'):
            text = baseNormalize(text)
            base = text.lower()
            base = IGNORE_REGEX.sub('', base)
            base = NON_WORD_REGEX.sub('-', base)
            base = MULTIPLE_DASHES_REGEX.sub('-', base)
            base = EXTRA_DASHES_REGEX.sub('', base)
            base = cropName(base)
            yield base
