"=============================================================================
" FILE: autoload/unite/source/citation.vim
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

"-----------------------------------------------------------------------
" {{{ Initialise
let s:save_cpo = &cpo
set cpo&vim

call unite#util#set_default('g:citation_vim_mode', "zotero")
call unite#util#set_default('g:citation_vim_zotero_version', 4)
call unite#util#set_default('g:citation_vim_zotero_path', "~/Zotero")
call unite#util#set_default('g:citation_vim_zotero_attachment_path', "~/Zotero/library")
call unite#util#set_default('g:citation_vim_et_al_limit', 5)
call unite#util#set_default('g:citation_vim_collection', "")
call unite#util#set_default('g:citation_vim_outer_prefix', "[")
call unite#util#set_default('g:citation_vim_inner_prefix', "@")
call unite#util#set_default('g:citation_vim_suffix', "]")
call unite#util#set_default('g:citation_vim_description_format', "{type}∶ {key} ˝{title}˝ ☆{author}☆ ₍{date}₎")
call unite#util#set_default('g:citation_vim_description_fields', ["type", "key", "title", "author", "date"])
call unite#util#set_default('g:citation_vim_key_format', "")
call unite#util#set_default('g:citation_vim_highlight_dash', "‾⁻−₋‐⋯┄–—―∼┈─▭▬┉━┅₌⁼‗")
call unite#util#set_default('g:citation_vim_highlight_bar', "‖│┃┆∥┇┊┋")
call unite#util#set_default('g:citation_vim_highlight_bracket', "⊂〔₍⁽⊃〕₎⁾")
call unite#util#set_default('g:citation_vim_highlight_arrow', "◀◁<‹▶▷>›")
call unite#util#set_default('g:citation_vim_source_wrap', "【】")
call unite#util#set_default('g:citation_vim_highlight_colon', "∶∷→⇒≫")
call unite#util#set_default('g:citation_vim_highlight_blob', "♯♡◆◇◊○◎●◐◑∗∙⊙⊚⌂★☺☻▪■□▢▣▤▥▦▧▨▩")
call unite#util#set_default('g:citation_vim_highlight_tiny', "、。‸₊⁺∘♢☆☜☞♢☼")
call unite#util#set_default('g:citation_vim_highlight_text', "″‴‶‷")

let s:script_path = escape( expand( '<sfile>:p:h' ), '\' )
let s:plugin_path = escape(expand('<sfile>:h:h:h:h'), '\')
let s:main_path = s:plugin_path . '/python/citation_vim/citation.py'

let s:has_supported_python = 0
if has('python3')"
    try
        exe 'py3file ' . s:main_path
        let s:has_supported_python = 3
    catch 
        echo "Citation.vim Error:" 
        echo "Python3 failed to load citation.py"
    endtry
elseif has('python')"
    try
        exe 'pyfile ' . s:main_path
        let s:has_supported_python = 2
    catch 
        echo "Citation.vim Error:" 
        echo "Python2 failed to load citation.py"
    endtry
else
    echo "Citation.vim unavailable:"
    echo "requires python 2 or 3 and Vim 7.3+"
endif


"-----------------------------------------------------------------------}}}
" {{{ Sources
let s:citation_source = {
\ 'name' : 'citation',
\ 'description' : 'display citation sources',
\}

let s:citation_collection_source = {
\ 'name' : 'citation_collection',
\ 'description' : 'search citation collection',
\}

let s:sub_sources = [
\ "abstract",
\ "author",
\ "combined",
\ "date",
\ "doi",
\ "file",
\ "isbn",
\ "publication",
\ "key",
\ "key_inner",
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

"-----------------------------------------------------------------------}}}
" {{{ Get source from python
function! s:get_source(source, field, args)
    if len(a:args) > 0
        let l:searchkeys = a:args[0]
    else
        let l:searchkeys = ""
    endif

    let l:out = []
    if s:has_supported_python == 3
        try
            let l:out = py3eval("Citation.connect()")
        catch 
            echo "Citation.vim Error:" 
            echo "Python3 connection error"
        endtry
    elseif s:has_supported_python == 2
        try
            let l:out = pyeval("Citation.connect()")
        catch 
            echo "Citation.vim Error:" 
            echo "Python2 connection error"
        endtry
    endif
    return l:out
endfunction

"-----------------------------------------------------------------------}}}
" {{{ List collections
function! s:citation_collection_source.gather_candidates(args, context)
  call unite#print_message('[Citation] collections')
  return map(s:get_source('citation_collection', '', ''), '{
\   "word"   : v:val,
\   "source" : s:citation_collection_source.name,
\   "kind": ["command"],
\   "action__command": s:set_collection(v:val),
\   "action__type": ": ",
\   "action__text": v:val,
\   "action__path": v:val,
\   "action__directory": fnamemodify(v:val, ":h"),
\ }')
endfunction

function! s:set_collection(c)
  return printf("let g:citation_vim_collection='%s'", a:c)
endfunction

"-----------------------------------------------------------------------}}}
" {{{ List sources
function! s:citation_source.gather_candidates(args, context)
    call unite#print_message('[Citation] citation sources')
    return map(s:sub_sources, '{
  \   "word"   : v:val,
  \   "source" : s:citation_source.name,
  \   "kind"   : "source",
  \   "action__source_name" : "citation/" . v:val,
  \ }')
endfunction

"-----------------------------------------------------------------------}}}
" {{{ Build all sub_sources programatically.
function! s:construct_sources(sub_sources)
    for sub_source in a:sub_sources
        exec "let s:citation_source_" . sub_source . " = {
        \       'name': 'citation/" . sub_source . "',
        \	      'default_action' : 'insert',
        \       'hooks': {},
        \       'syntax': 'uniteSource__citation',
        \      	'action_table' : {
        \	      	'preview' : {
        \		      	'description' : 'preview : Combined citation info {word}',
        \			      'is_quit' : 0,
        \      		}
        \	      }
        \     }"
        exec "function! s:citation_source_" . sub_source . ".hooks.on_syntax(args, context)
        \  \n   call s:hooks.syntax()
        \  \n endfunction"
        exec "function! s:citation_source_" . sub_source . ".gather_candidates(args,context)
        \  \n   return s:map_entries('citation','" . sub_source . "',a:args)
        \  \n endfunction"
        exec "function! s:citation_source_" . sub_source . ".action_table.preview.func(candidate)
        \  \n execute a:candidate.action__command
        \  \n endfunction"
    endfor
endfunction
call s:construct_sources(s:sub_sources)

function! s:map_entries(source, field, args)
    return map(s:get_source(a:source, a:field, a:args),'{
    \   "word": v:val[1],
    \   "source": a:source . "/" . a:field,
    \   "kind": ["word","file","uri","command"],
    \   "action__text": v:val[0],
    \   "action__path": v:val[2],
    \   "action__command": s:set_message(v:val[3]),
    \ }')
endfunction

"-----------------------------------------------------------------------}}}
" {{{ Override built gather_candidates for key and url
function! s:citation_source_key.gather_candidates(args,context)
    let l:prefix = g:citation_vim_outer_prefix . g:citation_vim_inner_prefix
    let l:suffix = g:citation_vim_suffix
    return map(s:get_source('citation', "key", a:args),'{
    \   "word": v:val[1],
    \   "source": "citation/key",
    \   "kind": ["word","file","uri","command"],
    \   "action__text": l:prefix . v:val[0] . l:suffix,
    \   "action__path": v:val[2],
    \   "action__command": s:set_message(v:val[3]),
    \ }')
endfunction

function! s:citation_source_key_inner.gather_candidates(args,context)
    let l:prefix = g:citation_vim_inner_prefix
    return map(s:get_source('citation', "key", a:args),'{
    \   "word": v:val[1],
    \   "source": "citation/key",
    \   "kind": ["word","file","uri","command"],
    \   "action__text": l:prefix . v:val[0],
    \   "action__path": v:val[2],
    \   "action__command": s:set_message(v:val[3]),
    \ }')
endfunction


function! s:citation_source_url_gather_candidates(args, context)
    return map(s:get_source('citation', "url", a:args),'{
    \   "word": v:val[1],
    \   "source": "citation/url",
    \   "kind": ["word","file","uri","command"],
    \   "action__text": v:val[0],
    \   "action__path": v:val[0],
    \   "action__command": s:set_message(v:val[3]),
    \ }')
endfunction

"-----------------------------------------------------------------------}}}
" {{{ Set prompt message
function! s:set_message(m)
    return printf('echo "%s"', a:m)
endfunction

"-----------------------------------------------------------------------}}}
" {{{ Return source and sub-sources to Unite.
function! unite#sources#citation#define()
    let l:sources = [s:citation_source, s:citation_collection_source]
    for sub_source in s:sub_sources
        let l:sources += [s:citation_source_{sub_source}]
    endfor
    return l:sources
endfunction

"-----------------------------------------------------------------------}}}
" {{{ Syntax
let s:hooks = {}
function! s:hooks.syntax()
  let arrow = g:citation_vim_highlight_arrow
  let source_field = g:citation_vim_source_wrap
  let blob = g:citation_vim_highlight_blob
  let colon = g:citation_vim_highlight_colon
  let tiny = g:citation_vim_highlight_tiny
  let bar = g:citation_vim_highlight_bar
  let dash = g:citation_vim_highlight_dash
  let bracket = g:citation_vim_highlight_bracket
  let text = g:citation_vim_highlight_text

  execute "syntax region uniteSource__Citation_Text start=/[" . text . "]/ end=/[" . text . "]/
        \ contains=uniteSource__Citation_Field,uniteSource__Citation_Split
        \ ,uniteSource__Citation_Arrow, uniteSource__Citation_Bar,uniteSource__Citation_Bracket
        \ containedin=uniteSource__Citation"
  execute "syntax region uniteSource__Citation_Source start=/[" . source_field . "]/ end=/[" . source_field . "]/
	 		        \ containedin=uniteSource__Citation"
  execute 'syntax match uniteSource__Citation_Colon "\<\w*[' . colon . ']"
			        \ contained containedin=uniteSource__Citation'
  execute "syntax region uniteSource__Citation_Bracket start=/[" . bracket . "]/ end=/[" . bracket . "]/
			        \ containedin=uniteSource__Citation"
  execute "syntax region uniteSource__Citation_Arrow start=/[" . arrow . "]/ end=/[" . arrow . "]/
			        \ containedin=uniteSource__Citation"
  execute "syntax region uniteSource__Citation_Blob start=/[" . blob . "]/ end=/[" . blob . "]/
			        \ containedin=uniteSource__Citation"
  execute "syntax region uniteSource__Citation_Tiny start=/[" . tiny . "]/ end=/[" . tiny . "]/
			        \ containedin=uniteSource__Citation"
  execute "syntax region uniteSource__Citation_Bar start=/[" . bar . "]/ end=/[" . bar . "]/
			        \ containedin=uniteSource__Citation"
  execute "syntax region uniteSource__Citation_Dash start=/[" . dash . "]/ end=/[" . dash . "]/
			        \ containedin=uniteSource__Citation"
  syntax match uniteSource__Citation_Key "\<[\S-]\+\d\{4}[\S-]*\>\|\<\S*\d\{4}\S\+\>" contained
			        \ containedin=uniteSource__Citation
              \ contains=uniteSource__Citation_Year
  syntax match uniteSource__Citation_Split "\.\{2}" contained
			        \ containedin=uniteSource__Citation
  syntax match uniteSource__Citation_Year "\d\{4}" contained

  highlight default link uniteSource__Citation_Colon Type
  highlight default link uniteSource__Citation_Text Comment
  highlight default link uniteSource__Citation_Key Special
  highlight default link uniteSource__Citation_Bracket Number
  highlight default link uniteSource__Citation_Source Error
  highlight default link uniteSource__Citation_Arrow Underlined
  highlight default link uniteSource__Citation_Bar Conditional
  highlight default link uniteSource__Citation_Blob Define
  highlight default link uniteSource__Citation_Dash Function
  highlight default link uniteSource__Citation_Year Define
  highlight default link uniteSource__Citation_Split SpecialComment
  highlight default link uniteSource__Citation_Tiny Identifier
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
