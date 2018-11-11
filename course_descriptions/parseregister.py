import sys
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice, TagExtractor
# pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from courseregisterparser import CourseRegisterParser
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams

# main


def main(argv):
    import getopt

    def usage():
        print('usage: %s [-d] [-p pagenos] [-m maxpages] [-P password] [-o output] '
              '[-n] [-A] [-D writing_mode] [-M char_margin] [-L line_margin] [-W word_margin] '
              '[-c codec] file ...' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dp:m:P:o:nAD:M:L:W:c:')
    except getopt.GetoptError:
        return usage()
    if not args:
        return usage()
    # debug option
    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = None
    codec = 'utf-8'
    pageno = 1
    showpageno = True
    laparams = LAParams()
    for (k, v) in opts:
        if k == '-d':
            debug += 1
        elif k == '-p':
            pagenos.update(int(x) - 1 for x in v.split(','))
        elif k == '-m':
            maxpages = int(v)
        elif k == '-P':
            password = v
        elif k == '-o':
            outfile = v
        elif k == '-n':
            laparams = None
        elif k == '-A':
            laparams.all_texts = True
        elif k == '-D':
            laparams.writing_mode = v
        elif k == '-M':
            laparams.char_margin = float(v)
        elif k == '-L':
            laparams.line_margin = float(v)
        elif k == '-W':
            laparams.word_margin = float(v)
        elif k == '-c':
            codec = v
    #
    CMapDB.debug = debug
    PDFResourceManager.debug = debug
    PDFDocument.debug = debug
    PDFParser.debug = debug
    PDFPageInterpreter.debug = debug
    PDFDevice.debug = debug
    #
    rsrcmgr = PDFResourceManager()

    if outfile:
        outfp = file(outfile, 'w')
    else:
        outfp = sys.stdout

    device = CourseRegisterParser(
        rsrcmgr, outfp, codec=codec, laparams=laparams)

    for fname in args:
        fp = file(fname, 'rb')
        process_pdf(rsrcmgr, device, fp, pagenos,
                    maxpages=maxpages, password=password)
        fp.close()
    device.close()
    outfp.close()
    return


if __name__ == '__main__':
    sys.exit(main(sys.argv))
