```sh
cat original.tex | python main.py > translated.tex
```

`original.tex`

```
\documentclass{article}

\usepackage{amsmath}
\usepackage{amsfonts}

\def\Q{\mathbb{Q}}

\begin{document}
	
hello $\Q$ world
	
\end{document}
```

`translated.tex`

```
\documentclass{article}

\usepackage{amsmath}
\usepackage{amsfonts}



\begin{document}
	
hello $\mathbb{Q}$ world
	
\end{document}
```

