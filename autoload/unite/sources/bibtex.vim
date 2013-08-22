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
"
function! unite#sources#bibtex#define() "{{{
  return s:source
endfunction "}}}

let s:source = {
      \ 'name': 'bibtex',
      \ }

function! s:source.gather_candidates(args,context)
    let bib_src = unite#util#system(g:unite_bibtex_articles_directory . '/bibtex_source.py')
    let lines = split(bib_src,'\n')
    let key = []
    let desc = []
    for line in lines
        let i = stridx(line,',')
        let k = line[:i-1]
        let d = line[(i+2):]
        call add(key,k)
        call add(desc,d)
    endfor
    return map(key,'{
    \   "word"   : desc[v:key],
    \   "source" : "bibtex",
    \   "kind"   : "word",
    \   "action__text" : v:val,
    \ }')
endfunction

" vim: foldmethod=marker
