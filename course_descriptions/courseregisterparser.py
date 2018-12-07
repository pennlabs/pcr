import sys
import re
from pdfminer.pdfdevice import PDFDevice, PDFTextDevice
from pdfminer.pdffont import PDFUnicodeNotDefined
from pdfminer.pdftypes import LITERALS_DCT_DECODE
from pdfminer.pdfcolor import LITERAL_DEVICE_GRAY, LITERAL_DEVICE_RGB
from pdfminer.layout import LTContainer, LTPage, LTText, LTLine, LTRect, LTPolygon
from pdfminer.layout import LTFigure, LTImage, LTChar, LTTextLine, LTTextBox, LTTextGroup
from pdfminer.utils import apply_matrix_pt, mult_matrix
from pdfminer.utils import enc, bbox2str, create_bmp

from cStringIO import StringIO
from pdfminer.converter import PDFConverter

import simplejson as json


def getOrElse(val, default=""): return val if val else default

# warning: potential confusion between this and models.Course


class Course:
    def __init__(self, description, title):
        self.description, self.title = description, title

    def titlematch(self):
        titlematch = re.match(
            "\s*(\d\d\d)\.\s*(\([^()]*\))?\s*(.*?)\.?\s*(\(.\))?\s*$", self.title)
        #titlematch = re.match("(\d\d\d)\.\s(\([^()]*\))?\s?([^()]*)\.\s?(\(.\))?", str(self.title))
        if not titlematch:
            print >> sys.stderr, "!!! REGEX ERROR:", self.title, "|", self.description
            return None
        else:
            ###num = self.title.split(".")[0]
            return titlematch.groups()  # num, crosslist, title, mysterycode

    def __str__(self):
        titlematch = self.titlematch()
        if not titlematch:
            return ""
        num, crosslist, title, mysterycode = titlematch
        return "\n".join(["#### " + num,
                          "## " + getOrElse(crosslist),
                          "## " + title,
                          "## " + getOrElse(mysterycode),
                          "## " + self.title,
                          self.description])

    def encode(self):
        titlematch = self.titlematch()
        if not titlematch:
            return None
        num, crosslist, title, mysterycode = titlematch
        description = self.description.strip()
        try:
            description += "\n\n(" + mysterycodedict[mysterycode[1]] + ")"
        except:
            pass
        return {"num": num, "crosslist": getOrElse(crosslist), "title": title,
                "offercode": getOrElse(mysterycode), "title": self.title,
                "description": description}


mysterycodedict = {
    "A": "Course offered in fall term only.",
    "B": "Course offered in spring term only.",
    "C": "One-term course offered either term.",
    "D": "Two terms. Student may enter either term. Credit is given for either term.",
    "E": "Two terms. Student must enter first term. Credit is given only on the completion of both terms.",
    "F": "Two terms. Student may enter either term. Credit is given only on the completion of both terms.",
    "G": "Two terms. Student must enter first term. Credit is given for first term without the second term.",
    "H": "Course offered fall even-numbered years.",
    "I": "Course offered fall odd-numbered years.",
    "J": "Course offered spring even-numbered years.",
    "K": "Course offered spring odd-numbered years.",
    "L": "Course offered in summer term only.",
    "M": "Course not offered every year."
}


class ParsedTextLine:
    def __init__(self, line="", title="", endsection=False):
        self.line, self.title, self.endsection = line, title, endsection

    def __add__(self, that):
        ptl = ParsedTextLine()
        ptl.line = self.line + that.line
        ptl.title = self.title + that.title
        ptl.endsection = that.endsection
        return ptl


def parseTextLine(textline):
    # LTChar extends LTText, has extra data; LTAnon extends LTText, is annoying
    texts = [child for child in textline if isinstance(child, LTText)]
    letters = [child for child in texts if isinstance(child, LTChar)]
    line = "".join(letter.text for letter in texts)
    line = line.replace(chr(10), "")  # remove end-of-line backspaces
    endsection = line.endswith("  ")
    line = line.strip() + " "  # ("*\n\n" if endsection else " ")
    title = "".join(
        letter.text for letter in letters if letter.get_size() > 12)

    return ParsedTextLine(line, title, endsection)


class CourseRegisterParser(PDFConverter):

    def __init__(self, rsrcmgr, outfp, codec='utf-8', pageno=1, laparams=None):
        PDFConverter.__init__(self, rsrcmgr, outfp,
                              codec=codec, pageno=pageno, laparams=laparams)
        self.textlines = []

    def write(self, text):
        self.outfp.write(text.encode(self.codec, 'ignore'))

    def receive_layout(self, ltpage):
        print >> sys.stderr, "page %d" % ltpage.pageid

        def getTextLines(item):
            if isinstance(item, LTTextLine):
                yield item
            elif isinstance(item, LTContainer):
                for child in item:
                    for line in getTextLines(child):
                        yield line

        self.textlines.extend(parseTextLine(x) for x in getTextLines(ltpage))

    def close(self):
        print >> sys.stderr, "closing..."
        # divide self.textlines into sections (if line.endsection, end a section)
        sections = []
        newsection = True
        for line in self.textlines:
            if newsection:
                sections.append(ParsedTextLine())
            sections[-1] += line
            newsection = line.endsection
        sections[-1].endsection = True

        # divide sections into courses (if len(section.title) > 0, start a course)
        coursetexts = []
        for section in sections:
            if len(section.title.strip()) > 0 or len(coursetexts) == 0:
                coursetexts.append(ParsedTextLine())
            coursetexts[-1] += section + ParsedTextLine(line="\n\n")

        courses = [Course(ptl.line, ptl.title) for ptl in coursetexts]

        # self.write( "\n".join(str(x) for x in courses))
        self.write(json.dumps([x.encode() for x in courses]))
        self.write('\f')
        return
