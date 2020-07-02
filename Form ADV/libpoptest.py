import pdfparser.poppler as pdf
import sys

crd = '161709'
d=pdf.Document(crd + '.pdf')
#print 'No of pages', d.no_of_pages
for p in d:
    #print 'Page', p.page_no, 'size =', p.size
    for f in p:
        #print ' '*1,'Flow'
        for b in f:
            #print ' '*2,'Block', 'bbox=', b.bbox.as_tuple()
            for l in b:
                #print ' '*3, l.text.encode('UTF-8'), '(%0.2f, %0.2f, %0.2f, %0.2f)'% l.bbox.as_tuple()
                #assert l.char_fonts.comp_ratio < 1.0
                for i in range(len(l.text)):
                    print(l.text[i].encode('UTF-8'), '(%0.2f, %0.2f, %0.2f, %0.2f)'% l.char_bboxes[i].as_tuple())
