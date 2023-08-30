import chardet


def utf8list_to_unicode(utf8_list):
    unicode_list = []
    for utf8_string in utf8_list:
        print(utf8_string)
        print(chardet.detect(utf8_string.encode('utf-8')))
        unicode_string = utf8_string.encode('utf-8')
        unicode_list.append(unicode_string)
    return unicode_list
