unite-bibtex
============

a BibTeX source for unite.vim

## Usage

If you understand Japanese see [this](http://termoshtt.hatenablog.com/)

 1. Install Unite for vim
 1. Install plugin (aka NeoBundle/pathogen)
 1. `sudo easy_install pybtex`
 1. Set variable `let g:unite_bibtex_bib_files=["~/papers/bib/all.bib"]`
 1. `:Unite bibtex` in vim
 

## Troubleshooting

Check that your bibtex file parses correctly by using [this script](https://gist.github.com/Tarrasch/7983895)
