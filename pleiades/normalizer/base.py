import re
import string
from unicodedata import normalize, decomposition

# Latin characters with accents, etc.
mapping = {
138 : 's', 140 : 'O', 142 : 'z', 154 : 's', 156 : 'o', 158 : 'z', 159 : 'Y',
192 : 'A', 193 : 'A', 194 : 'A', 195 : 'a', 196 : 'A', 197 : 'A', 198 : 'E',
199 : 'C', 200 : 'E', 201 : 'E', 202 : 'E', 203 : 'E', 204 : 'I', 205 : 'I',
206 : 'I', 207 : 'I', 208 : 'D', 209 : 'N', 210 : 'O', 211 : 'O', 212 : 'O',
213 : 'O', 214 : 'O', 215 : 'x', 216 : 'O', 217 : 'U', 218 : 'U', 219 : 'U',
220 : 'U', 221 : 'Y', 223 : 's', 224 : 'a', 225 : 'a', 226 : 'a', 227 : 'a',
228 : 'a', 229 : 'a', 230 : 'e', 231 : 'c', 232 : 'e', 233 : 'e', 234 : 'e',
235 : 'e', 236 : 'i', 237 : 'i', 238 : 'i', 239 : 'i', 240 : 'd', 241 : 'n',
242 : 'o', 243 : 'o', 244 : 'o', 245 : 'o', 246 : 'o', 248 : 'o', 249 : 'u',
250 : 'u', 251 : 'u', 252 : 'u', 253 : 'y', 255 : 'y',
305 : 'i', 8216 : '\'', 8217 : '\'', 8220:'"', 8221:'"'
}

# On OpenBSD string.whitespace has a non-standard implementation
# See http://dev.plone.org/plone/ticket/4704 for details
whitespace = ''.join([c for c in string.whitespace if ord(c) < 128])
allowed = string.ascii_letters + string.digits + string.punctuation + whitespace

# Define and compile static regexes
IGNORE_REGEX = re.compile(r"['\"()]")
NON_WORD_REGEX = re.compile(r"[\W\-]+")
DANGEROUS_CHARS_REGEX = re.compile(r"[!#$%&()*+,/:;<=>?@\\^_{|}\[\]~]+")
MULTIPLE_DASHES_REGEX = re.compile(r"\-+")
EXTRA_DASHES_REGEX = re.compile(r"(^\-+)|(\-+$)")
RIVER_REGEX = re.compile(r" fl\.$")
ISLAND_REGEX = re.compile(r" Ins\.$", re.I)
ISLAND_GROUP_REGEX = re.compile(r" Inss\.$", re.I)
MAX_LENGTH = 120


def cropName(base, maxLength=MAX_LENGTH):
    baseLength = len(base)

    index = baseLength
    while index > maxLength:
        index = base.rfind('-', 0, index)

    if index == -1 and baseLength > maxLength:
        base = base[: maxLength]

    elif index > 0:
        base = base[: index]

    return base

def baseNormalize(text):
    """
    This method is used for normalization of unicode characters to the base ASCII
    letters. Output is ASCII encoded string (or char) with only ASCII letters,
    digits, punctuation and whitespace characters. Case is preserved.

      >>> baseNormalize(123)
      '123'

      >>> baseNormalize(u'\u0fff')
      'fff'

      >>> baseNormalize(u"foo\N{LATIN CAPITAL LETTER I WITH CARON}")
      'fooI'
    """
    if not isinstance(text, basestring):
        # This most surely ends up in something the user does not expect
        # to see. But at least it does not break.
        return repr(text)

    text = text.strip()

    res = u''
    for ch in text:
        if ch in allowed:
            # ASCII chars, digits etc. stay untouched
            res += ch
        else:
            ordinal = ord(ch)
            if mapping.has_key(ordinal):
                # try to apply custom mappings
                res += mapping.get(ordinal)
            elif decomposition(ch):
                normalized = normalize('NFKD', ch).strip()
                # string may contain non-letter chars too. Remove them
                # string may result to more than one char
                res += ''.join([c for c in normalized if c in allowed])
            else:
                # hex string instead of unknown char
                res += "%x" % ordinal
        
    return res.encode('ascii')


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
        suffix = None
        for re in [RIVER_REGEX, ISLAND_REGEX, ISLAND_GROUP_REGEX]:
            m = re.search(label)
            if m:
                suffix = m.group()
                label = re.sub('', label)
                break

        for text in label.split('/'):
            if suffix is not None:
                text = text + suffix
            text = baseNormalize(text)
            base = text.lower()
            base = IGNORE_REGEX.sub('', base)
            base = NON_WORD_REGEX.sub('-', base)
            base = MULTIPLE_DASHES_REGEX.sub('-', base)
            base = EXTRA_DASHES_REGEX.sub('', base)
            base = cropName(base)
            yield base
