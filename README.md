unite-bibtex
============

a BibTeX source for unite.vim

Use your markdown documents as complete document manager - open referenced pdfs
and urls directly from your citations or from a citation list. Browse all
citation details, notes and abstracts within vim. Yank, insert or preview just
about any of them.

Best used with zotero automatically downloading pdfs, and automatically
exporting with zotero_better_bibtex. Standard zotero bibtex will probably break
everything...


### Sources

This version of the plugin provides a *lot* of sources.

bibtex/key
- returns the bibtex key string like [@smith2004] to be used as a reference.
- customisable prefix and suffix for latex/pandoc citations

bibtex/file
- Returns the file attached to a citation, great for opening pdfs from vim
  directly, using the start action.
- If there are multiple files it just returns the first one.

bibtex/combined
- Preview all available citation data on one page.

And everything else! Some more useful than others...

bibtex/abstract
bibtex/annote
bibtex/author
bibtex/doi
bibtex/isbn
bibtex/journal
bibtex/language
bibtex/month
bibtex/pages
bibtex/publisher
bibtex/shorttitle
bibtex/title
bibtex/type
bibtex/volume
bibtex/year

### Examples mappings:

Set a unite leader:
nmap <leader>u [unite]
nnoremap [unite] <nop>

To insert a citation:
nnoremap <silent>[unite]c       :<C-u>Unite -buffer-name=bibtex   -start-insert -default-action=append      bibtex<cr>

To immediately open/yank/browse a file or url from citation under the cursor:

    nnoremap <silent><leader>cc :<C-u>Unite -buffer-name=bibtex -input=<C-R><C-W> -default-action=start -force-immediately bibtex/file<cr>
    nnoremap <silent><leader>cU :<C-u>Unite -buffer-name=bibtex -input=<C-R><C-W> -default-action=yank -force-immediately bibtex/url<cr>
    nnoremap <silent><leader>cu :<C-u>Unite -buffer-name=bibtex -input=<C-R><C-W> -default-action=start -force-immediately bibtex/url<cr>
    nnoremap <silent><leader>cC :<C-u>Unite -buffer-name=bibtex -input=<C-R><C-W> -default-action=yank -force-immediately bibtex/file<cr>
    nnoremap <silent><leader>cf :<C-u>Unite -buffer-name=bibtex -input=<C-R><C-W> -default-action=file -force-immediately bibtex/file<cr>

To preview, append, yank citation data from unite:

    nnoremap <silent>[unite]c  :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/key<cr>
    nnoremap <silent>[unite]cf :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=start  -auto-preview bibtex/file<cr>
    nnoremap <silent>[unite]cF :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/file<cr>
    nnoremap <silent>[unite]cu :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=start  -auto-preview bibtex/url<cr>
    nnoremap <silent>[unite]cU :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/url<cr>
    nnoremap <silent>[unite]ca :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/author<cr>
    nnoremap <silent>[unite]cp :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/publisher<cr>
    nnoremap <silent>[unite]cj :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/journal<cr>
    nnoremap <silent>[unite]cd :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/doi<cr>
    nnoremap <silent>[unite]ct :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/title<cr>
    nnoremap <silent>[unite]cy :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/year<cr>
    nnoremap <silent>[unite]ci :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/isbn<cr>
    nnoremap <silent>[unite]cn :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/annote<cr>
    nnoremap <silent>[unite]cb :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=append -auto-preview bibtex/abstract<cr>
    nnoremap <silent>[unite]cc :<C-u>Unite -buffer-name=bibtex -start-insert -default-action=preview              bibtex/combined<cr>



### Requirements

- Vim with python2 or python3 scripting enabled.
- [unite.vim](https://github.com/Shougo/unite.vim)
- [pybtex](http://pypi.python.org/pypi/pybtex): A BibTeX-compatible bibliography processor in Python

### Usage

1. Install [pybtex](http://pypi.python.org/pypi/pybtex) `sudo easy_install pybtex`
1. Install [unite.vim](https://github.com/Shougo/unite.vim)
1. Install this plugin
1. Set variable 

    let g:unite_bibtex_bib_files=["/path/to/your/bib/file/library.bib"]

1. Set your citation suffix and prefix. Pandoc markdown style is the default.

    let g:unite_bibtex_bib_prefix = "[@"
    let g:unite_bibtex_bib_suffix = "]"

### Tweaks 

Customise the unite display, using the names of bibtex sources and a python format string:

    let g:unite_bibtex_description_format = "{}: {} \"{}\" {} ({})"
    let g:unite_bibtex_description_fields = ["type", "key", "title", "author", "year"]

or this one is nice for showing journal/publisher (citations rarely have both):

    let g:unite_bibtex_description_format', "{}: {} \'{}\' {} |{}{}|"
    let g:unite_bibtex_description_fields', ["type", "key", "title", "author", "publisher", "journal"]

All regions inside (), [], ||, "", '' or <> will be highlighted as will anything
like "key2001name" or "word:"

### Troubleshooting

You can correct your .bib file with `pybtex-convert`:

    pybtex-convert /path/to/your.bib out.bib
