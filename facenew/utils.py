import re

_pre_punct_re = re.compile(r'[\t :!"#$%&\'()*\-/<=>?@\[\\\]^_`{|},]+')
_post_punct_re = re.compile(r'[\t :!"#$%&\'()*\-/<=>?@\[\\\]^`{|},]+')
_mulit_underscore = re.compile(r'[__]+')


def slug(text, delim=u"_"):
    result = []
    for word in _pre_punct_re.split(text.lower()):
        word = word.encode("translit/long/ascii", "replace")
        if word:
            result.append(word)
    s = unicode(delim.join(result))
    return _mulit_underscore.sub("_", _post_punct_re.sub(delim, s))