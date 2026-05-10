# Converting markdown to PDFs with pandoc on macOS

# Overview

Converting `markdown` to `pdf`’s on macOS Big Sur with `pandoc` installed from `brew`.

# Details

Install `pandoc` with brew:

```
brew install pandoc
```

Install `basictex` with brew:

```
brew install --cask basictex
```

Symlink the `pdflatex` binary into `/usr/local/bin`:

```
jemurray@jasons-mbp posts % sudo ln -s /Library/Tex/Distributions/.DefaultTeX/Contents/Programs/x86_64/pdflatex /usr/local/bin
```

Example conversion with images:

```
cat kc3-2020-obj1.md kc3-2020-obj2.md 
  \ | sed 's/(\/images\//(/g' 
  \ | pandoc -f markdown 
  \ --resource-path=../../static/images/ 
  \ -t pdf 
  \ -o ~/kc3-2020-writeup.pdf
```