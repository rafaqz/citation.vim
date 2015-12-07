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

let s:source_abstract = {
    \ 'action_table': {},
    \ 'name': 'bibtex/abstract',
    \ }
let s:source_author = {
    \ 'action_table': {},
    \ 'name': 'bibtex/author',
    \ }
let s:source_doi = {
    \ 'action_table': {},
    \ 'name': 'bibtex/doi',
    \ }
let s:source_file = {
    \ 'action_table': {},
    \ 'name': 'bibtex/key',
    \ }
let s:source_isbn = {
    \ 'action_table': {},
    \ 'name': 'bibtex/isbn',
    \ }
let s:source_journal = {
    \ 'action_table': {},
    \ 'name': 'bibtex/isbn',
    \ }
let s:source_key = {
    \ 'action_table': {},
    \ 'name': 'bibtex/key',
    \ }
let s:source_language = {
    \ 'action_table': {},
    \ 'name': 'bibtex/language',
    \ }
let s:source_journal = {
    \ 'action_table': {},
    \ 'name': 'bibtex/language',
    \ }
let s:source_publisher = {
    \ 'action_table': {},
    \ 'name': 'bibtex/publisher',
    \ }
let s:source_title = {
    \ 'action_table': {},
    \ 'name': 'bibtex/title',
    \ }
let s:source_uri = {
    \ 'action_table': {},
    \ 'name': 'bibtex/url',
    \ }
let s:source_year = {
    \ 'action_table': {},
    \ 'name': 'bibtex/year',
    \ }

function! unite#sources#bibtex#define() 
  return [
         \ s:source_author,
         \ s:source_abstract,
         \ s:source_doi,
         \ s:source_file, 
         \ s:source_isbn,
         \ s:source_journal,
         \ s:source_key,
         \ s:source_language,
         \ s:source_publisher,
         \ s:source_title,
         \ s:source_uri,
         \ s:source_year
         \ ]
endfunction 

pyfile <sfile>:h:h:h:h/src/unite_bibtex.py

function! s:get_entries(field)
    let l:candidates = []
python << EOF
import vim
bibpaths = vim.eval("g:unite_bibtex_bib_files")
entries = unite_bibtex.get_entries(bibpaths)
for k, v in entries.items():
    vim.command("call add(l:candidates,['{}','{}'])".format(v.filename, v.desc))
EOF
    return l:candidates
endfunction

function! s:map_entries(field) 
    return map(s:get_entries(a:field),'{
    \   "word": v:val[1],
    \   "source": "bibtex",
    \   "kind": "word",
    \   "action__text": v:val[0],
    \ }')
endfunction

function! s:source_key.gather_candidates(args,context)
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

function! s:source_uri.gather_candidates(args,context)
    return map(s:get_entries("url"),'{
    \   "word": v:val[1],
    \   "source": "bibtex/uri",
    \   "kind": ["word","uri"],
    \   "action__text": v:val[0],
    \   "action__path": v:val[0],
    \ }')
endfunction

function! s:source_abstract.gather_candidates(args,context)
  return s:map_entries("abstract")
endfunction

function! s:source_author.gather_candidates(args,context)
  return s:map_entries("author")
endfunction

function! s:source_doi.gather_candidates(args,context)
  return s:map_entries("doi")
endfunction

function! s:source_isbn.gather_candidates(args,context)
  return s:map_entries("isbn")
endfunction

function! s:source_journal.gather_candidates(args,context)
  return s:map_entries("journal")
endfunction

function! s:source_language.gather_candidates(args,context)
  return s:map_entries("language")
endfunction

function! s:source_publisher.gather_candidates(args,context)
  return s:map_entries("publisher")
endfunction

function! s:source_title.gather_candidates(args,context)
  return s:map_entries("title")
endfunction

function! s:source_year.gather_candidates(args,context)
  return s:map_entries("year")
endfunction


let &cpo = s:save_cpo
unlet s:save_cpo
" vim: foldmethod=marker
