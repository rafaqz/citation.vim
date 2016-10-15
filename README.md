citation.vim
============

A citation source for unite.vim

(https://github.com/rafaqz/citation.vim)

Citation.vim imports zotero databases with better_bibtex citation keys if
available, or exported bibtex files. It can insert keys and many other fields,
open attached pdfs and urls, or search zoteros fulltext database.

It allows you to use your documents as file managers - open referenced pdfs
and urls directly from your citations or from a citation list. Browse all
citation details, notes and abstracts within vim. Yank, insert or preview.
Pass keywords to filter results with a zoteros fulltext search.

![Citation.vim screenshot](screenshot.png?raw=true "Citation.vim screenshot")

Many thanks to termoshtt for unite-bibtex and smathot for gnotero and LibZotero code.


### Sources

This plugin provides a *lot* of unite sources.

citation/key
- returns citation key string like [@smith2004] to be used as a reference.
- change the customisable prefix and suffix to produce latex/pandoc etc. citation styles

citation/file
- Returns the file attached to a citation, great for opening pdfs from vim
  directly, using the start action.
- If there are multiple files it just returns the first one.

citation/combined
- Preview all available citation data on one page.

The full list:

- citation/abstract
- citation/author
- citation/combined
- citation/date
- citation/doi
- citation/file
- citation/isbn
- citation/publication
- citation/key
- citation/key_inner
- citation/language
- citation/issue
- citation/notes
- citation/pages
- citation/publisher
- citation/tags
- citation/title
- citation/type
- citation/url
- citation/volume

You can also enter `:Unite citation` in vim for the full list of sources.

`:Unite citation_collection` will list zotero collections: select one to filter results.

No matter what source is selected, execute/edit and preview commands will always
echo combined information for the citation, and file will always use the
attached pdf/epub file path. This is useful for setting open/show info key
commands to use within unite, no matter what source is being browsed - see
the example mappings for how to do this.


### Usage

1. Install [unite.vim](https://github.com/Shougo/unite.vim)
2. Install this plugin in vim however you like to do that.
3. Choose your source

  If you're using bibtex install [pybtex](http://pypi.python.org/pypi/pybtex)

  ```bash
  sudo easy_install pybtex
  ```

  Set variables:

  ```vimscript
  let g:citation_vim_bibtex_file="/path/to/your/bib/file/library.bib"
  let g:citation_vim_mode="bibtex"
  ```

  To use [zotero](https://www.zotero.org/)
    Set variables:

  ``` vimscript
  let g:citation_vim_mode="zotero"
  let g:citation_vim_zotero_path="/path/to/your/zotero/7XX8XX72/zotero_folder/"
  ```

  The zotero path is quite variable accross different systems, just make sure it
  contains the file `zotero.sqlite`


  And optionally:

  ```
  let g:citation_vim_collection" = 'your_zotero_collection'
  ```
  Although this can be set on the fly with :Unite citation_colletion

4. Set a cache path:

  ```vimscript
    let g:citation_vim_cache_path='~/.vim/your_cache_path'
  ```

5. Set your citation suffix and prefix. Pandoc markdown style is the default.

  ```vimscript
  let g:citation_vim_outer_prefix="["
  let g:citation_vim_inner_prefix="@"
  let g:citation_vim_suffix="]"
  ```

6. Set the et al. limit. If the number of authors is greater than the limit only
   the first author with `et al.` appended is shown or printed in case of
   `citation/author`. (Default: 5)

  ```vimscript
  let g:citation_vim_et_al_limit=2
  ```

7. Set some mappings. Copy and paste the following examples into your vimrc to get started.


### Example mappings:

Set a unite leader:
nmap <leader>u [unite]
nnoremap [unite] <nop>

To insert a citation:

```vimscript
nnoremap <silent>[unite]c       :<C-u>Unite -buffer-name=citation
-start-insert -default-action=append      citation/key<cr>
```

To immediately open a file from a citation under the cursor:

```vimscript
nnoremap <silent>[unite]co :<C-u>Unite -input=<C-R><C-W> -default-action=start -force-immediately citation/file<cr>
```

Or open a url from a citation under the cursor:

nnoremap <silent><leader>cu :<C-u>Unite -input=<C-R><C-W> -default-action=start -force-immediately citation/url<cr>


To browse the file folder from a citation under the cursor:

```vimscript
nnoremap <silent>[unite]cf :<C-u>Unite -input=<C-R><C-W> -default-action=file -force-immediately citation/file<cr>
```

To view all citation information from a citation under the cursor:

```vimscript
nnoremap <silent>[unite]ci :<C-u>Unite -input=<C-R><C-W> -default-action=preview -force-immediately citation/combined<cr>


To preview, append, yank any other citation data you want from unite:

```vimscript

nnoremap <silent>[unite]cp :<C-u>Unite -default-action=yank citation/your_source_here<cr>
```


#### Search fulltext!!

Search for word by appending them after the command and a colon:

Search for the word under the cursor:

```vimscript
nnoremap <silent>[unite]cs :<C-u>Unite  -default-action=yank  citation/key:<C-R><C-W><cr>
```
Search for selected words in visual mode (notice that spaces have to be escaped) :

```vimscript
vnoremap <silent>[unite]cs :<C-u>exec "Unite  -default-action=start citation/key:" . escape(@*,' ') <cr>
```
Type search terms in the prompt:

```vimscript
nnoremap <silent>[unite]cx :<C-u>exec "Unite  -default-action=start citation/key:" . escape(input('Search Key : '),' ') <cr>
```

`:Unite citation` for a full list of sources...

#### Open files or show info from any source

This autocomand set Control-o to open files and Control-i to show info

```vimscript
autocmd FileType unite call s:unite_my_settings()
function! s:unite_my_settings()
  nnoremap <silent><buffer><expr> <C-o> unite#do_action('start')
  imap     <silent><buffer><expr> <C-o> unite#do_action('start')
  nnoremap <silent><buffer><expr> <C-i> unite#do_action('preview')
  imap     <silent><buffer><expr> <C-i> unite#do_action('preview')
endfunction
```

### Tweaks

Customise the unite display, using the names of citation sources and a python
format string (the {} braces will be replaced by the sources):

```vimscript
let g:citation_vim_description_format = "{}∶ {} \˝{}\˝ ₋{}₋ ₍{}₎"
let g:citation_vim_description_fields = ["type", "key", "title", "author", "year"]
```

or this one is nice for showing journal/publisher (citations rarely have both):

```vimscript
let g:citation_vim_description_format="{}→ ′{}′ ₊{}₊ │{}{}│"
let g:citation_vim_description_fields=["key", "title", "author", "publisher", "journal"]
```

You might have noticed the weird characters in the description format string.
They are used for highlighting sections, to avoid confusion with
normal characters that might be in the citation.

To change description highlighting characters, copy and paste characters from this list:
- Quotes                  ″‴‶‷    
- Brackets                ⊂〔₍⁽     ⊃〕₎⁾ 
- Arrows                  ◀◁<‹    ▶▷>› 
- Blobs                   ♯♡◆◇◊○◎●◐◑∗∙⊙⊚⌂★☺☻▪■□▢▣▤▥▦▧▨▩
- Tiny                    、。‸₊⁺∘♢☆☜☞♢☼
- Bars                    ‖│┃┆∥┇┊┋
- Dashes                  ‾⁻−₋‐⋯┄–—―∼┈─▭▬┉━┅₌⁼‗

- And use these like a colon after words (notice that's not a normal colon)
        ∶∷→⇒≫

Long lines will occasionally break the display colors. It's a quirk of how unite
shortens lines.


### Troubleshooting

You can correct your .bib file with `pybtex-convert`:

    pybtex-convert /path/to/your.bib out.bib
