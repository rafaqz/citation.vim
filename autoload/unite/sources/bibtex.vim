"=============================================================================
" FILE: autoload/unite/source/bibtex.vim
" AUTHOR:  Toshiki TERAMUREA <toshiki.teramura@gmail.com>
" Last Modified: 8 Oct 2015.
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

let s:save_cpo = &cpo
set cpo&vim

call unite#util#set_default('g:unite_bibtex_bib_files', [])
call unite#util#set_default('g:unite_bibtex_bib_prefix', "")

let s:source_desc = {
      \ 'action_table': {},
      \ 'name': 'bibtex',
      \ }

let s:source_file = {
      \ 'action_table': {},
      \ 'name': 'bibtex/file',
      \ }

let s:source_uri= {
      \ 'action_table': {},
      \ 'name': 'bibtex/uri',
      \ }

function! unite#sources#bibtex#define() 
  return [s:source_desc, s:source_file, s:source_uri]
endfunction 

pyfile <sfile>:h:h:h:h/src/unite_bibtex.py


function! s:source_desc.gather_candidates(args,context)
    let l:candidates = []
python << EOF
import vim
bibpaths = vim.eval("g:unite_bibtex_bib_files")
entries = unite_bibtex.get_entries(bibpaths)
for k, v in entries.items():
    vim.command("call add(l:candidates,['{}','{}'])".format(k, v.desc))
EOF
    return map(l:candidates,'{
    \   "word": v:val[1],
    \   "source": "bibtex",
    \   "kind": "word",
    \   "action__text": "[@" . v:val[0] . "]",
    \ }')
endfunction


function! s:source_file.gather_candidates(args,context)
    let l:candidates = []
python << EOF
import vim
bibpaths = vim.eval("g:unite_bibtex_bib_files")
entries = unite_bibtex.get_entries(bibpaths)
for k, v in entries.items():
    vim.command("call add(l:candidates,['{}','{}'])".format(v.filename, v.desc))
EOF
    return map(l:candidates,'{
    \   "word": v:val[1],
    \   "source": "bibtex_file",
    \   "kind": ["word","file", "uri"],
    \   "action__text": v:val[0],
    \   "action__path": v:val[0],
    \ }')
endfunction


function! s:source_uri.gather_candidates(args,context)
    let l:candidates = []
python << EOF
import vim
bibpaths = vim.eval("g:unite_bibtex_bib_files")
entries = unite_bibtex.get_entries(bibpaths)
for k, v in entries.items():
    vim.command("call add(l:candidates,['{}','{}'])".format(v.url, v.desc))
EOF
    return map(l:candidates,'{
    \   "word": v:val[1],
    \   "source": "bibtex_uri",
    \   "kind": ["word","uri"],
    \   "action__text": v:val[0],
    \   "action__path": v:val[0],
    \ }')
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
" vim: foldmethod=marker
