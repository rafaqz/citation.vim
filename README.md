unite-bibtex
============

a BibTeX source for unite.vim

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
