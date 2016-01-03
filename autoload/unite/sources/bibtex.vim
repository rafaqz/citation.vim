"=============================================================================
" FILE: autoload/unite/source/bibtex.vim
" AUTHOR:  Rafael Schouten <rafaelschouten@gmail.com>, 
" Forked From: unite-bibtex, Toshiki TERAMUREA
" Last Modified: 8 Dec 2015.
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

call unite#util#set_default('g:unite_bibtex_file_paths', "")
call unite#util#set_default('g:unite_bibtex_file_format', "bibtex")
call unite#util#set_default('g:unite_bibtex_outer_prefix', "[")
call unite#util#set_default('g:unite_bibtex_inner_prefix', "@")
call unite#util#set_default('g:unite_bibtex_suffix', "]")
call unite#util#set_default('g:unite_bibtex_description_format', "{}∶ {} ˝{}˝ ☆{}☆ ₍{}₎")
call unite#util#set_default('g:unite_bibtex_description_fields', ["type", "key", "title", "author", "date"])

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )

let s:has_supported_python = 0
if has('python3')"
    let s:has_supported_python = 3
elseif has('python')"
    let s:has_supported_python = 2
endif
let s:plugin_path = escape(expand('<sfile>:h:h:h:h'), '\')

if s:has_supported_python == 3
    echo s:plugin_path
    exe 'py3file ' . s:plugin_path . '/python/unite_bibtex/connect.py'
elseif s:has_supported_python == 2
    exe 'pyfile ' . s:plugin_path . '/python/unite_bibtex/connect.py'
else
    function! s:DidNotLoad()
        echohl WarningMsg|echomsg "Unite bibtex unavailable: requires Vim 7.3+"|echohl None
    endfunction
    command! call s:DidNotLoad()
    call s:DidNotLoad()
endif

let s:sub_sources = [
\ "abstract",
\ "author",
\ "combined",
\ "date",
\ "doi",
\ "file",
\ "isbn",
\ "journal",
\ "key",
\ "language",
\ "issue",
\ "notes",
\ "pages",
\ "publisher",
\ "tags",
\ "title",
\ "type",
\ "url",
\ "volume"
\ ]

" Build source variable and function programatically for all sub_sources.
function! s:construct_sources(sub_sources)
    for sub_source in a:sub_sources
        exec "let s:source_" . sub_source . " = { 
        \       'action_table': {}, 
        \       'name': 'bibtex/" . sub_source . "', 
        \       'hooks': {},
        \       'syntax': 'uniteSource__Bibtex'
        \     }"
        exec "function! s:source_" . sub_source . ".hooks.on_syntax(args, context)
        \  \n   call s:hooks.syntax()
        \  \n endfunction"
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
    return map(s:get_source(a:field),'{
    \   "word": v:val[1],
    \   "source": "bibtex",
    \   "kind": "word",
    \   "action__text": v:val[0],
    \ }')
endfunction

" Get bibtex entries for a given field.
function! s:get_source(field)
    let l:out = []
    if s:has_supported_python == 3
      let l:out = py3eval("uniteBibtex.connect()")
    elseif s:has_supported_python == 2
      let l:out = pyeval("uniteBibtex.connect()")
    endif
    return l:out
endfunction

" Override default gather_candidates function where necessary.
function! s:source_key.gather_candidates(args,context)
    let prefix = g:unite_bibtex_outer_prefix . g:unite_bibtex_inner_prefix
    let suffix = g:unite_bibtex_suffix
    return map(s:get_source("key"),'{
    \   "word": v:val[1],
    \   "source": "bibtex/key",
    \   "kind": "word",
    \   "action__text": prefix . v:val[0] . suffix,
    \ }')
endfunction
function! s:source_file.gather_candidates(args,context)
    return map(s:get_source("file"),'{
    \   "word": v:val[1],
    \   "source": "bibtex/file",
    \   "kind": ["word","file", "uri"],
    \   "action__text": v:val[0],
    \   "action__path": v:val[0],
    \ }')
endfunction
function! s:source_url.gather_candidates(args,context)
    return map(s:get_source("url"),'{
    \   "word": v:val[1],
    \   "source": "bibtex/url",
    \   "kind": ["word","uri"],
    \   "action__text": v:val[0],
    \   "action__path": v:val[0],
    \ }')
endfunction

let s:hooks = {}
function! s:hooks.syntax()
  syntax region uniteSource__Bibtex_Text start=+[˝‘’‛“”‟′″‴‵‶‷]+ end=+[˝‘’‛“”‟′″‴‵‶‷]\|.[∶∷→⇒≫⊂⊃〔〕₍₎⁽⁾◁▷◀▶<>‹›♯♡♢◆◇◊○◎●◐◑∗∘∙⊙⊚⌂★☆☜☞☺☻☼₊⁺▪■□▢▣▤▥▦▧▨▩]+ 
        \ contains=uniteSource__Bibtex_Field,uniteSource__Bibtex_Split
        \ ,uniteSource__Bibtex_Arrow, uniteSource__Bibtex_Bar,uniteSource__Bibtex_Bracket   
        \ containedin=uniteSource__Bibtex
  syntax match uniteSource__Bibtex_Key "\<[\w-]\+\d\{4}[\w-]*\>\|\<\w*\d\{4}\w\+\>" contained
			        \ containedin=uniteSource__Bibtex
              \ contains=uniteSource__Bibtex_Year
  syntax region uniteSource__Bibtex_Field start='【' end='】'
			        \ containedin=uniteSource__Bibtex
  syntax match uniteSource__Bibtex_Type "\<\w*[∶∷→⇒≫]" 
			        \ contained containedin=uniteSource__Bibtex
  syntax region uniteSource__Bibtex_Bracket start='[⊂〔₍⁽]' end='[⊃〕₎⁾]' 
			        \ containedin=uniteSource__Bibtex
  syntax region uniteSource__Bibtex_Arrows start='[◀◁<‹]' end='[▶▷>›]' 
			        \ containedin=uniteSource__Bibtex
  syntax region uniteSource__Bibtex_Blob start='[♯♡◆◇◊○◎●◐◑∗∙⊙⊚⌂★☺☻▪■□▢▣▤▥▦▧▨▩]' end='[♯♡◆◇◊○◎●◐◑∗∙⊙⊚⌂★☺☻▪■□▢▣▤▥▦▧▨▩]' 
			        \ containedin=uniteSource__Bibtex
  syntax region uniteSource__Bibtex_Tiny start='[、。‸₊⁺∘♢☆☜☞♢☼]' end='[、。‸₊⁺∘☆☜☞♢☼]'
			        \ containedin=uniteSource__Bibtex
  syntax region uniteSource__Bibtex_Bar start='[‖│┃┆∥┇┊┋]' end='[‖│┃┆∥┇┊┋]'
			        \ containedin=uniteSource__Bibtex
  syntax region uniteSource__Bibtex_Dash start='[‾⁻−₋‐⋯┄–—―∼┈─▭▬┉━┅₌⁼‗]' end='[‾⁻−₋‐⋯┄–—―∼┈─▭▬┉━┅₌⁼‗]'
			        \ containedin=uniteSource__Bibtex
  syntax match uniteSource__Bibtex_Split "\.\{2}" contained
			        \ containedin=uniteSource__Bibtex
  syntax match uniteSource__Bibtex_Year "\d\{4}" contained
  highlight default link uniteSource__Bibtex_Type Type
  highlight default link uniteSource__Bibtex_Text Comment
  highlight default link uniteSource__Bibtex_Key Special
  highlight default link uniteSource__Bibtex_Bracket Number
  highlight default link uniteSource__Bibtex_Field Error
  highlight default link uniteSource__Bibtex_Arrows Underlined
  highlight default link uniteSource__Bibtex_Bar Conditional
  highlight default link uniteSource__Bibtex_Blob Define
  highlight default link uniteSource__Bibtex_Dash Function
  highlight default link uniteSource__Bibtex_Year Define
  highlight default link uniteSource__Bibtex_Split SpecialComment
  highlight default link uniteSource__Bibtex_Tiny Identifier
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
