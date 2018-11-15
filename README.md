citation.vim
============

A citation source for [unite.vim](https://github.com/Shougo/unite.vim)

(https://github.com/rafaqz/citation.vim)

Citation.vim imports Zotero databases or exported bibtex/biblatex files. It can
insert keys and many other fields, open attached pdfs and urls.

Citation.vim allows you to create a workflow from within your documents. You can
open referenced pdfs or url directly from citations, and view all citation
details, notes and abstracts within vim or nvim. You can also use Zoteros
full-text search to pre-filter items based on attachment text.

![Citation.vim screenshot](screenshot.png?raw=true "Citation.vim screenshot")

Many thanks to termoshtt for unite-bibtex and smathot for gnotero and LibZotero code.

_Warning: the concept of this plugin is fundamentally a hack. It uses Zotero
databases in ways they are not intended to be used (in the name of brute speed and
unmatched utility, of course), and bibtex/biblatex files that are problematic in
terms of their structural consistency. This plugin should work for Zotero 5 or
biblatex files in vim with python 2 or 3 on Linux, in English. I test the hell
out that setup and use it most days. Other setups may work fine, or they may
break._

If you have problems, please open an issue on github and include the error output
from vim.

### Sources

This plugin provides a *lot* of unite sources. Some important ones are:

citation/key
- returns citation key string like [@smith2004] to be used as a reference.
- customise the prefix and suffix to produce latex/pandoc etc. citation styles.

citation/file
- Returns the file attached to a citation, great for opening pdfs from vim
  directly, using the 'start' action.
- If there are multiple files it returns the first one.

citation/combined
- Preview all available citation data on one page.


The full list:

| Source                  | Output                                                               |
| ----------------------- | -------------------------------------------------------------------- |
| citation                | list sources                                                         |
| citation/abstract       | absract                                                              |
| citation/author         | all authors, combined with rules set in g:citation_vim_et_al_limit   |
| citation/combined       | all fields combined in an info page                                  |
| citation/date           | year of publication                                                  |
| citation/doi            | doi                                                                  |
| citation/duplicate_keys | key from filter items that have duplicate keys                       |
| citation/file           | the first listed attachment that is a pdf, epub or ps file           |
| citation/isbn           | isbn                                                                 |
| citation/publication    | name of journal, magazine etc                                        |
| citation/key            | key from bibtex, generated, of from zotero. default format is [@key] |
| citation/key_inner      | inner key, default format is @key                                    |
| citation/language       | language                                                             |
| citation/issue          | issue                                                                |
| citation/notes          | all attached notes, joined                                           |
| citation/pages          | pages                                                                |
| citation/publisher      | publisher                                                            |
| citation/tags           | all tags, comma separated                                            |
| citation/title          | title                                                                |
| citation/type           | type of item                                                         |
| citation/url            | url                                                                  |
| citation/volume         | volume                                                               |
| citation/zotero_key     | the raw key used by zotero                                           |
| citation_collection     | (yes underscore not slash) list Zotero collection to filter results. |



Whichever source is selected, execute/edit and preview commands will always echo
combined information for the citation, and file will always use the attached
pdf/epub file path. This is useful for setting open/show info key commands to
use within unite - see the example mappings for how to do this.

### Installation

1. Install [unite.vim](https://github.com/Shougo/unite.vim)
2. Install this plugin in vim however you like to do that.
3. Choose your source

    If you're using bibtex 
  
    * install [pybtex](http://pypi.python.org/pypi/pybtex)

      ``` bash
      easy_install pybtex
      ```

    * Set variables:

      ```vimscript
      let g:citation_vim_bibtex_file="/path/to/your/bib/file/library.bib"
      let g:citation_vim_mode="bibtex"
      ```

    To use [zotero](https://www.zotero.org/)
 
    * Set variables:

      ```vimscript
      let g:citation_vim_mode="zotero" (default)
      let g:citation_vim_zotero_path="/path/to/your/zotero/7XX8XX72/zotero_folder/" ("~/Zotero" is default)
      let g:citation_vim_zotero_version=5 (5 is the Default, zotero 4 is no longer supported)
      ```

      The zotero path is quite variable accross different systems, just make sure it
      contains the file `zotero.sqlite`

    * If you have set a "Linked Attachment Base Directory" in zotero
      (in Preferences\Files and Folders) you will need to set:

      ```vimscript
      let g:citation_vim_zotero_attachment_path="/your/linked/attachment/base/directory" ("default ~/Zotero/library")
      ```

    * If you don't have the better bibtex plugin and you want
      readable keys (like smith2010Sometitle), set a key formatter. This will not
      produce fixed keys like the better-bibtex plugin, so make sure to manage your
      duplicates (use Unite citation/duplicate_keys to check) and watch for key
      changes after editing author, date or title in zotero. Author and Title can be
      in lower case or sentence case.

      ```vimscript
      let g:citation_vim_key_format="{author}{date}{title}"
      ```

      Key cleanup is set ot match zoteros default Bibtex.js/Biblatex.js translator
      files. If you need to change these, you can also set:

      ```vimscript
      let g:citation_vim_key_title_banned_regex = "\\b(a|an|the|some|from|on|in|to|of|do|with|der|die|das|ein|eine|einer|eines|einem|einen|un|une|la|le|l|el|las|los|al|uno|una|unos|unas|de|des|del|d)\\W")
      let g:citation_vim_key_clean_regex = "[^A-Za-z0-9\!\$\&\*\+\-\.\/\:\;\<\>\?\[\]\^\_\`\|]+")
      ```

    * And optionally:

      ```
      let g:citation_vim_collection" = 'your_zotero_collection'
      ```

      Although this can be set on the fly with :Unite citation_collection

4. Set a cache path:

  ```vimscript
  let g:citation_vim_cache_path='~/.vim/your_cache_path'
  ```
  

5. Set your citation suffix and prefix. This pandoc markdown style is the default:

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
  
7. The default order results are displayed in was recently reversed so your
  recent additions are allways at the top. If you want to keep the old
  behaviour, set:

  ```vimscript
  let g:citation_vim_reverse_order=0 
  ```

8. Set some mappings. Copy and paste the following examples into your vimrc to get started.

### Key mappings:

Set a unite leader:

```vimscript
nmap <leader>u [unite]
nnoremap [unite] <nop>
```

To insert a citation:

```vimscript
nnoremap <silent>[unite]c       :<C-u>Unite -buffer-name=citation-start-insert -default-action=append      citation/key<cr>
```

To immediately open a file from a citation under the cursor:

```vimscript
nnoremap <silent>[unite]co :<C-u>Unite -input=<C-R><C-W> -default-action=start -force-immediately citation/file<cr>
```

Or open a url from a citation under the cursor:

```vimscript
nnoremap <silent><leader>cu :<C-u>Unite -input=<C-R><C-W> -default-action=start -force-immediately citation/url<cr>
```

To browse the file folder from a citation under the cursor:

```vimscript
nnoremap <silent>[unite]cf :<C-u>Unite -input=<C-R><C-W> -default-action=file -force-immediately citation/file<cr>
```

To view all citation information from a citation under the cursor:

```vimscript
nnoremap <silent>[unite]ci :<C-u>Unite -input=<C-R><C-W> -default-action=preview -force-immediately citation/combined<cr>
```

To preview, append, yank any other citation data you want from unite:

```vimscript
nnoremap <silent>[unite]cp :<C-u>Unite -default-action=yank citation/your_source_here<cr>
```


#### Search fulltext

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

This autocomand sets Control-o to open files and Control-i to show info

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
let g:citation_vim_description_fields = ["key", "author", "doi", "journal", "whateveryouwant"]
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

```sh
pybtex-convert /path/to/your.bib out.bib
```

If you have other problems, open an issue on github and include the error output
from vim. Please pull the latest changes first, and include your vim/nvim
version and zotero versions in the issue. Attaching your bib(la)tex file may also be
helpful if using the bibtex/biblatex backend.

