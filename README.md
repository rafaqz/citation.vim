citation.vim
============

A citation source for unite.vim

Citation.vim Imports zotero databases (with better_bibtex citation keys if
available) or exported bibtex files and inserts/runs/does whatever you want with
them using Unite.vim.

It also allows you to use your documents as file managers - open referenced pdfs
and urls directly from your citations or from the citation list. Browse all
citation details, notes and abstracts within vim. Yank, insert or preview .

![Citation.vim screenshot](screenshot.png?raw=true "Citation.vim screenshot")

Many thanks to termoshtt for unite-bibtex and smathot for gnotero and LibZotero code.


### Sources

This plugin provides a *lot* of unite sources.

citation/key
- returns the citation key string like [@smith2004] to be used as a reference.
- customisable prefix and suffix to produce latex/pandoc etc. citation styles

citation/file
- Returns the file attached to a citation, great for opening pdfs from vim
  directly, using the start action.
- If there are multiple files it just returns the first one.

citation/combined
- Preview all available citation data on one page.

And everything else! Some more useful than others...

citation/abstract
citation/author
citation/date
citation/doi
citation/isbn
citation/issue
citation/journal
citation/language
citation/month
citation/note
citation/pages
citation/publisher
citation/tags
citation/title
citation/type
citation/volume

### Usage

1. Install [unite.vim](https://github.com/Shougo/unite.vim)
1. Install this plugin in vim however you like to do that.
1. If you're using bibtex install [pybtex](http://pypi.python.org/pypi/pybtex)

    sudo easy_install pybtex

  Set variables:

      let g:citation_vim_file_path=["/path/to/your/bib/file/library.bib"]
      let g:citation_vim_file_format="citation"

1. To use [zotero](http://pypi.python.org/pypi/pybtex)
  Set variables:

    let g:citation_vim_file_path=["/path/to/your/zotero/7XX8XX72/zotero/folder/"]
    let g:citation_vim_file_format="zotero"

1. Set your citation suffix and prefix. Pandoc markdown style is the default.

    let g:citation_vim_outer_prefix="["
    let g:citation_vim_inner_prefix="@"
    let g:citation_vim_suffix="]"

1. Set some mappings. Copy and paste the following examples into your vimrc to get started.


### Examples mappings:

Set a unite leader:
nmap <leader>u [unite]
nnoremap [unite] <nop>

To insert a citation:

    nnoremap <silent>[unite]c       :<C-u>Unite -buffer-name=citation   -start-insert -default-action=append      bibtex<cr>

To immediately open a file or url from a citation under the cursor:

    nnoremap <silent><leader>co :<C-u>Unite -input=<C-R><C-W> -default-action=start -force-immediately citation/file<cr>

To immediately browse the folder from a citation under the cursor:

    nnoremap <silent><leader>cf :<C-u>Unite -input=<C-R><C-W> -default-action=file -force-immediately citation/file<cr>

To view all citation information from a citation under the cursor:

    nnoremap <silent><leader>ci :<C-u>Unite -input=<C-R><C-W> -default-action=preview -force-immediately citation/combined<cr>


To preview, append, yank citation data from unite:

    nnoremap <silent>[unite]c  :<C-u>Unite -buffer-name=citation -default-action=append  -auto-preview bibtex/key<cr>
    nnoremap <silent>[unite]cF :<C-u>Unite -buffer-name=citation -default-action=append  -auto-preview bibtex/file<cr>
    nnoremap <silent>[unite]ca :<C-u>Unite -buffer-name=citation -default-action=append  -auto-preview bibtex/author<cr>
    nnoremap <silent>[unite]cp :<C-u>Unite -buffer-name=citation -default-action=append  -auto-preview bibtex/publisher<cr>
    nnoremap <silent>[unite]cj :<C-u>Unite -buffer-name=citation -default-action=append  -auto-preview bibtex/journal<cr>
    nnoremap <silent>[unite]ct :<C-u>Unite -buffer-name=citation -default-action=append  -auto-preview bibtex/title<cr>
    nnoremap <silent>[unite]cn :<C-u>Unite -buffer-name=citation -default-action=append  -auto-preview bibtex/annote<cr>
    nnoremap <silent>[unite]cb :<C-u>Unite -buffer-name=citation -default-action=append  -auto-preview bibtex/abstract<cr>
    nnoremap <silent>[unite]cI :<C-u>Unite -buffer-name=citation -default-action=preview -auto-preview bibtex/combined<cr>

To preview, append, yank citation data from unite:
    nnoremap <silent>[unite]cc :<C-u>Unite -buffer-name=citation -start-insert -default-action=preview              bibtex/combined<cr>




### Tweaks 

Customise the unite display, using the names of citation sources and a python format string:

    let g:citation_vim_description_format = "{}∶ {} \˝{}\˝ ₋{}₋ ₍{}₎"
    let g:citation_vim_description_fields = ["type", "key", "title", "author", "year"]

or this one is nice for showing journal/publisher (citations rarely have both):

    let g:citation_vim_description_format="{}→ ′{}′ ₊{}₊ │{}{}│"
    let g:citation_vim_description_fields=["key", "title", "author", "publisher", "journal"]

Highlighting picks up text between some weird characters. Nothing on the keyboard, as they will be in
the citation text too. 

Copy and paste characters from this list:
- Apostrophes and quotes  ˝‘’‛“”‟′″‴‵‶‷
- Brackets                ⊂〔₍⁽     ⊃〕₎⁾ 
- Arrows                  ◀◁<‹    ▶▷>› 
- Blobs                   ♯♡◆◇◊○◎●◐◑∗∙⊙⊚⌂★☺☻▪■□▢▣▤▥▦▧▨▩
- Tiny                    、。‸₊⁺∘♢☆☜☞♢☼
- Bars                    ‖│┃┆∥┇┊┋
- Dashes                  ‾⁻−₋‐⋯┄–—―∼┈─▭▬┉━┅₌⁼‗

- And use these like a colon after words (notice that's not a normal colon!)
        ∶∷→⇒≫ 

Long lines will occasionally break the display colors. It's a quirk of how unite
shortens lines.

### Troubleshooting

You can correct your .bib file with `pybtex-convert`:

    pybtex-convert /path/to/your.bib out.bib
