"=============================================================================
" FILE: build.vim
" AUTHOR:  Toshiki TERAMUREA <toshiki.teramura@gmail.com>
" Last Modified: 22 Aug 2013.
" License: MIT license  {{{
"     Permission is hereby granted, free of charge, to any person obtaining
"     a copy of this software and associated documentation files (the
"     "Software"), to deal in the Software without restriction, including
"     without limitation the rights to use, copy, modify, merge, publish,
"     distribute, sublicense, and/or sell copies of the Software, and to
"     permit persons to whom the Software is furnished to do so, subject to
"     the following conditions:
"
"     The above copyright notice and this permission notice shall be included
"     in all copies or substantial portions of the Software.
"
"     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
"     OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
"     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
"     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
"     CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
"     TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
"     SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
" }}}
"=============================================================================


" Variables
call unite#util#set_default('g:unite_bibtex_bib_files',[])


let s:source = {
      \ 'name': 'bibtex',
      \ }


function! s:source.gather_candidates(args,context)
    let l:candidates = []
python << EOF
import os.path
import vim
from pybtex.database.input import bibtex
from pybtex import errors


def _read_file(filename):
    errors.enable_strict_mode()
    parser = bibtex.Parser()
    return parser.parse_file(filename)


def _check_path(path):
    path = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(path):
        raise RuntimeError("file:%s not found" % path)
    return path


def entry_to_str(entry):
    try:
        persons = entry.persons[u'author']
        authors = [unicode(au) for au in persons]
    except:
        authors = [u'unknown']
    title   = entry.fields[u"title"] if u"title" in entry.fields else ""
    journal = entry.fields[u"journal"] if u"journal" in entry.fields else ""
    year    = entry.fields[u"year"] if u"year" in entry.fields else ""
    desc = u"%s %s %s(%s)" % (",".join(authors),title,journal,year)
    return desc.replace("'","").replace("\\","")


bibpath_list = vim.eval("g:unite_bibtex_bib_files")
for bibpath in bibpath_list:
    path = _check_path(bibpath)
    bibdata = _read_file(path)
    for key in bibdata.entries:
        try:
            k = key.encode("utf-8")
        except:
            print("encode fails")
            continue
        desc = entry_to_str(bibdata.entries[key]).encode("utf-8")
        vim.command("call add(l:candidates,['%s','%s'])" % (k,desc))
EOF
    return map(l:candidates,'{
    \   "word": v:val[1],
    \   "source": "bibtex",
    \   "kind": "word",
    \   "action__text": "\\cite{" . v:val[0] . "}",
    \ }')
endfunction


function! unite#sources#bibtex#define() 
    return s:source
endfunction 


" vim: foldmethod=marker
