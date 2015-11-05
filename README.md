unite-bibtex
============

a BibTeX source for unite.vim


### Sources

This version of the plugin provides three sources:

**bibtex**
- returns the bibtex key string like [@smith2004] to be used as a reference.
  @TODO setup variables for the prefix and suffix text so its customisable
  between latex/markdown etc.

**bibtex_file**
- Returns the file attached to a citation, great for opening pdfs from vim
  directly, using the start action.
- If there are multiple files it just returns the first one.
- Can’t handle colons in file data!

**bibtex_url**
- Returns the url for a citation, which you can also open from unite
  also using the start action, or insert, append etc.


### Examples mappings:

To insert a citation:
nnoremap <silent>[unite]c       :<C-u>Unite -buffer-name=bibtex   -start-insert -default-action=append      bibtex<cr>

To open a file or url from a citation:
nnoremap <silent>[unite]cf      :<C-u>Unite -buffer-name=bibtex   -start-insert -default-action=start       bibtex_file<cr>
nnoremap <silent>[unite]cu      :<C-u>Unite -buffer-name=bibtex   -start-insert -default-action=start       bibtex_uri<cr>

These mappings use unite to open a file or url immediately from the bibtex
key under the cursor, without actually opening a unite window. Helps navigating
to referenced documents without leaving vim.

nnoremap <silent><leader>cf :<C-u>Unite -buffer-name=bibtex -input=<C-R><C-W> -default-action=start -force-immediately bibtex_file<cr>
nnoremap <silent><leader>cu :<C-u>Unite -buffer-name=bibtex -input=<C-R><C-W> -default-action=start -force-immediately bibtex_uri<cr>


### Requirements

- [unite.vim](https://github.com/Shougo/unite.vim)
- [pybtex](http://pypi.python.org/pypi/pybtex): A BibTeX-compatible bibliography processor in Python

### Usage

 1. Install [pybtex](http://pypi.python.org/pypi/pybtex) `sudo easy_install pybtex`
 1. Install [unite.vim](https://github.com/Shougo/unite.vim)
 1. Install this plugin
 1. Set variable `let g:unite_bibtex_bib_files=["/path/to/your/bib/file/library.bib"]`
 1. `:Unite bibtex` in vim

### Troubleshooting

You can correct your .bib file with `pybtex-convert`:

```
pybtex-convert /path/to/your.bib out.bib
```

If you meet an import error of pybtex, please confirm your pybtex is installed into your system.
Python interpreter of vim usually uses system site-package, so you should install pybtex into your system directory.
