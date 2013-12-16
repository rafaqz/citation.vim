unite-bibtex
============

a BibTeX source for unite.vim

## Usage

If you understand japanese see [this](http://termoshtt.hatenablog.com/)

 0. Instll Unite for vim
 1. Install plugin (aka NeoBundle/pathogen)
 2. `sudo easy_install pybtex`
 3. Set variable `let g:unite_bibtex_bib_files=["~/papers/bib/all.bib"]`
 4. `:Unite bibtex` in vim
 

## Troubleshooting

Check that your bibtex file parses correctly by using [this script](https://gist.github.com/Tarrasch/7983895)
