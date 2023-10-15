import markdownify
import os


class cd:
    def __init__(self, new_path: str):
        self.path: str = new_path

    def __enter__(self):
        self.saved_path: str = os.getcwd()
        os.chdir(self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.saved_path)


class CustomMarkdownConverter(markdownify.MarkdownConverter):
    def convert_sup(self, el, text, convert_as_inline):
        markup = self.options["sup_symbol"]
        prefix, suffix, text = markdownify.chomp(text)
        if not text:
            return ""
        return "%s%s%s%s" % (prefix, markup, text, suffix)
