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
call unite#util#set_default('g:unite_bibtex_bib_prefix', "[@")
call unite#util#set_default('g:unite_bibtex_bib_suffix', "]")
call unite#util#set_default('g:unite_bibtex_description_format', "{}: {} \"{}\" {} ({})")
call unite#util#set_default('g:unite_bibtex_description_fields', ["type", "key", "title", "author", "year"])

let s:sub_sources = [
\ "abstract",
\ "annote",
\ "author",
\ "combined",
\ "doi",
\ "file",
\ "isbn",
\ "journal",
\ "key",
\ "language",
\ "month",
\ "pages",
\ "publisher",
\ "shorttitle",
\ "title",
\ "uri",
\ "volume",
\ "year"
\ ]

" Build source variable and function programatically for all sub_sources.
function! s:construct_sources(sub_sources)
    for sub_source in a:sub_sources
        exec "let s:source_" . sub_source . " = { 
        \       'action_table': {}, 
        \       'name': 'bibtex/" . sub_source . "' 
        \     }"
        exec "function! s:source_" . sub_source . ".gather_candidates(args,context) 
        \    \n   return s:map_entries('" . sub_source . "') 
        \    \n endfunction"
    endfor
endfunction

call s:construct_sources(s:sub_sources)

" Return all sources (bibtex/sub_source) to Unite.
function! unite#sources#bibtex#define() 
    let l:sources = []
    for sub_source in s:sub_sources
        let l:sources += [s:source_{sub_source}]
    endfor
    return l:sources
endfunction 

pyfile <sfile>:h:h:h:h/src/unite_bibtex.py

" Map entries for unite.
function! s:map_entries(field) 
    return map(s:get_entries(a:field),'{
    \   "word": v:val[1],
    \   "source": "bibtex",
    \   "kind": "word",
    \   "action__text": v:val[0],
    \ }')
endfunction

" Get bibtex entries for a given field.
function! s:get_entries(field)
    let l:candidates = []
    python import vim

python << endpython
bibpaths = vim.eval("g:unite_bibtex_bib_files")
desc_format = vim.eval("g:unite_bibtex_description_format")
desc_fields = vim.eval("g:unite_bibtex_description_fields")
field = vim.eval("a:field")
entries = unite_bibtex.get_entries(bibpaths)

def bibtex_description(entry):
    eval_fields = []
    for field in desc_fields:
        eval_fields += [eval("entry." + field)]
    return desc_format.format(*eval_fields)

for key, entry in entries.items():
    desc = bibtex_description(entry)
    vim.command("call add(l:candidates,['{}','{}'])".format(eval('entry.' + field), desc))
endpython

    return l:candidates
endfunction


" Override default gather_candidates function where necessary.
function! s:source_key.gather_candidates(args,context)
    let prefix = g:unite_bibtex_bib_prefix
    let suffix = g:unite_bibtex_bib_suffix
    return map(s:get_entries("key"),'{
    \   "word": v:val[1],
    \   "source": "bibtex/key",
    \   "kind": "word",
    \   "action__text": prefix . v:val[0] . suffix,
    \ }')
endfunction

function! s:source_file.gather_candidates(args,context)
    return map(s:get_entries("file"),'{
    \   "word": v:val[1],
    \   "source": "bibtex/file",
    \   "kind": ["word","file", "uri"],
    \   "action__text": v:val[0],
    \   "action__path": v:val[0],
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

let &cpo = s:save_cpo
unlet s:save_cpo
