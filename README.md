```sh
cat original.tex | python main.py > translated.tex
```

`original.tex`

```latex
\documentclass{article}

\usepackage{amsmath}
\usepackage{amsfonts}

\def\Q{\mathbb{Q}}

\begin{document}
	
hello $\Q$ world
	
\end{document}
```

`translated.tex`

```latex
\documentclass{article}

\usepackage{amsmath}
\usepackage{amsfonts}



\begin{document}
	
hello $\mathbb{Q}$ world
	
\end{document}
```

---

# Macro expansion

The engine has a expansion queue. Pops the first element of the queue and expands it. Then repeat this process until the queue is empty.

There is native macros:

* `\def`
* `\let`
* `\futurelet`
* `\expandafter`

and user defined macro.

The native macros are explained in the next section. In this section, we explain the expansion of user defined macros.

A user defined macro consist of three components:

* `Name`
* `Pattern`
* `Body`


The `name` is just a key to identify the macro. When `\name` is evaluated, the engine looks for `name`, check if is user defined macro and expands it.

The `Body` is a list of tokens. When the macro is expanded, replaces `#1, ..., #9` in `Body` by the corresponding argument and puts in the start of the expansion queue.

The `Pattern` is a list of tokens that schemes how to assign the arguments.

## Examples of patterns:

### Simple argument single token assigment

* `Pattern: [#1]`
* `Queue: [H, e, l, l, o]`

This assigns

* `argument 1: [H]`
* `Queue: [e, l, l, o]`

### Simple argument multiple token assigment
 
* `Pattern: [#1]`
* `Queue: [{, H, e, l, l, o}, W, o, r, l, d]`

This assigns

* `argument 1: [H, e, l, l, o]`
* `Queue: [W, o, r, l, d]`

#### Simple tokens pattern

* `Pattern: [H, e]`
* `Queue: [H, e, l, l, o]`

This assigns

* `Queue: [l, l, o]`

#### Simple tokens pattern fails

* `Pattern: [H, e]`
* `Queue: [h, e, l, l, o]`

This raises an error and assigns

* `Queue: undefined`


#### Argument before tokens pattern (1)

* `Pattern: [#1, W, o, r, l, d]`
* `Queue: [H, e, l, l, o, W, o, r, l, d]`

This assigns

* `argument 1: [H, e, l, l, o]`
* `Queue: [W, o, r, l, d]`


#### Argument before tokens pattern (2)

* `Pattern: [#1, W, o, r, l, d]`
* `Queue: [H, e, {, l, l, }, o, W, o, r, l, d]`

This assigns

* `argument 1: [H, e, {, l, l, }, o]`
* `Queue: [W, o, r, l, d]`


#### Argument before tokens pattern (3 - fails)

* `Pattern: [#1, W, o, r, l, d]`
* `Queue: [{, H, e, l, }, l , o, W, o, r, l, d]`

This raises an error and assigns

* `Queue: undefined

#### Argument before tokens pattern (4)

* `Pattern: [#1, W, o, r, l, d]`
* `Queue: [{, H, e, l, l , o, }, W, o, r, l, d]`

This assigns

* `argument 1: [H, e, l, l, o]`
* `Queue: [W, o, r, l, d]`


#### Argument before Argument (1)

* `Pattern: [#1, #2]`
* `Queue: [a, b, c]`

This assigns

* `argument 1: [a]`
* `argument 2: [b]`
* `Queue: [c]`

#### Argument before Argument (2)

* `Pattern: [#1, #2]`
* `Queue: [{, a, b, }, {, c, d, e, }, f]`

This assigns

* `argument 1: [a, b]`
* `argument 2: [c, d, e]`
* `Queue: [f]`

 
#### Argument, Tokens, Argument (1)

* `Pattern: [#1, a, t, #2]`
* `Queue: [H, e, l, l, o, a, t, W, o, r, l, d]`

This assigns

* `argument 1: [H, e, l, l, o]`
* `argument 2: [W, o, r, l, d]`
* `Queue: []`


#### Argument, Tokens, Argument (2)

* `Pattern: [#1, a, t, #2]`
* `Queue: [H, e, l, l, o, a, t, {, W, o, }, r, l, d]`

This assigns

* `argument 1: [H, e, l, l, o]`
* `argument 2: [W, o]`
* `Queue: [r, l, d]`

#### Tokens, Argument, Tokens, Argument, Tokens

* `Pattern: [N, a, m, e, :, #1, -, N, u, m, b, e, r, :, #2, .]`
* `Queue: [N, a, m, e, :, J, o, h, n, -, N, u, m, b, e, r, :, 1, 2, 3, .]`

This assigns

* `argument 1: [J, o, h, n]`
* `argument 2: [1, 2, 3]`
* `Queue: []`


---

 
# Native Macros

---

## `\def`


### Format:

`\def NameMacro PatternTokens... {BodyTokens...}`

defines the macro `NameToken` with the pattern `[TransformedPatternTokens...]` and the body `[TransformedBodyTokens...]`.

### Requirements:

`NameMacro`: Need to be a macro token. For example, `\this`.


### Internal:

Before: `[\def, MacroToken, PatternToken1, ..., {, BodyToken1, ..., }]`

After: `[]`


### Examples
`\def\removedotcom #1.com{#1}`


### Transformations:

In `PatternTokens` and `BodyTokens`, the `[#, #]` are transformed to `[#]` and `[#, (digit)]` to `[#digit].`

For example, `\def\meta{\def\macro##1{##1}}`. Defines a macro `\meta` as

* `Name: meta`
* `Pattern: []`
* `Body: [\def, \macro, #, 1, {, #, 1, }]`
 
When `\meta` is evaluated, defines `\macro` as

* `Name: macro`
* `Pattern: [#1]`
* `Body: [#1]` 


Another example, `\def\metameta{\def\meta{\def\macro####1{####1}}}`. Defines `\metameta` as

* `Name: metameta`
* `Pattern: []`
* `Body: [\def, \meta, {, \def, \macro, #, #, 1, {, #, #, 1, }, }]`

When `\metameta` is evaluated, defines `\meta` as

* `Name: meta`
* `Pattern: []`
* `Body: [\def, \macro, #, 1, {, #, 1, }]` 


---

## `\let`

### Format

`\let ToToken FromToken`
 
Define the macro `ToToken` same as `FromToken`.

### Requirements:

`ToToken`: Need to be a macro Token. For example, `\this`.

`FromToken`: Need to be a macro Token. For example, `\this`.


### Internal

Before: `[\let, ToMacro, FromMacro ]`

After: `[]`

### Examples

`\def\a{Hello world}\let\b\a` has the same effect as `\def\a{Hello world}\def\b{Hello world}`

---

## `\futurelet`

### Format

`\futurelet ToToken LastToken FromToken`

Define the macro `ToToken` same as `FromToken` and then expands LastToken


### Requirements


`ToToken`: Need to be a macro Token. For example, `\this`.

`FromToken`: Need to be a macro Token. For example, `\this`.


### Internal

Before: `[\futurelet, ToMacro, LastToken, FromMacro ]`

After: `[LastToken]`


---

## `\expandafter`

### Format

`\expandafter Token1 Token2`

If `Token2` is not a user defined macro, has the same effect as `Token1 Token2`.

If `Token2` is a user defined macro, replace `Token2` in the queue with the expansion of `Token2`.

### Internal

If `Token2` is not a user defined macro:

Before: `[\expandafter, Token1, Token2]`

After: `[Token1, Token2]`


If `Token2` is a user defined macro:

Before: `[\expandafter, Token1, Token2]`

After: `[Token1, ExpandedTokens2...]`

where ExpandedTokens2... is the result tokens of the expansion of Token2.

### Example:

`\def\a#1{(#1)}\def\b#1{h(ello #1)}\expandafter\a\b{world}` has the same effect as `\def\a#1{(#1)}\def\b#1{h(ello #1)}(h)(ello world)`