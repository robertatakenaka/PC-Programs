# coding=utf-8

from ...generics import fs_utils


class XHTMLDocument(object):

    def __init__(self, filename):
        self.file = fs_utils.File(filename)

    @property
    def body_content(self):
        if '<body' in self.file.content and '</body>' in self.file.content:
            body = self.file.content[:self.file.content.rfind('</body>')]
            body = body[body.find('<body'):]
            body = body[body.find('>')+1:]
            return body
