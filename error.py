class ParseError(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return str('ParseError: {} could not be parsed'.format(self.url))


if __name__ == '__main__':
    try:
        raise(ParseError('blog.nierunjie.site/atom.xml'))
    except ParseError as e:
        print(e)
