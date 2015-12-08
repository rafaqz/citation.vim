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

let s:has_supported_python = 0
if has('python3')"
    let s:has_supported_python = 3
elseif has('python')"
    let s:has_supported_python = 2
endif
let s:plugin_path = escape(expand('<sfile>:h:h:h:h'), '\')

if s:has_supported_python == 3
    echo s:plugin_path
    exe 'py3file ' . s:plugin_path . '/src/unite_bibtex.py'
elseif s:has_supported_python == 2
    exe 'pyfile ' . s:plugin_path . '/src/unite_bibtex.py'
else
    function! s:DidNotLoad()
        echohl WarningMsg|echomsg "Unite bibtex unavailable: requires Vim 7.3+"|echohl None
    endfunction
    command! call s:DidNotLoad()
    call s:DidNotLoad()
endif

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
\ "url",
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
        \  \n   return s:map_entries('" . sub_source . "') 
        \  \n endfunction"
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
    let l:out = []
    if s:has_supported_python == 3
      let l:out = py3eval("unite_bibtex.connect()")
    elseif s:has_supported_python == 2
      let l:out = pyeval("unite_bibtex.connect()")
    endif
    return l:out
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

function! s:source_url.gather_candidates(args,context)
    return map(s:get_entries("url"),'{
    \   "word": v:val[1],
    \   "source": "bibtex/url",
    \   "kind": ["word","uri"],
    \   "action__text": v:val[0],
    \   "action__path": v:val[0],
    \ }')
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
