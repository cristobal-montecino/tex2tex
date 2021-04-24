#!/usr/bin/python
from parse import parse

# def
assert parse('\\def\\newcommand#1#2{\\def#1{#2}}\\newcommand{\\hello}{hello world}\\hello world') == 'hello worldworld'

assert parse('\\def\\eat#1{}\eat hello') == 'ello'

assert parse('\\def\\eat#1{}\eat{hello}') == ''

assert parse('\\def\\parse user: #1, number: #2{Hello #1 (###2)}\\parse user: {John}, number: {123}') == 'Hello John (#123)'
assert parse('\\def\\parse user: #1, number: #2{Hello #1 (###2)}\\parse user: John, number: 123') == 'Hello John (#1)23'

assert parse('\\def\\defineDefineEat{\\def\\defineEat{\\def\\eat####1{}}\\defineEat}\\defineDefineEat\\eat hello') == 'ello'

code ='\\def\\a#1{\\def\\b##1##2##3##4{###1}\\b{a}{b}{c}{d}}\\a'
assert parse(code + '3') == 'c' and parse(code + '4') == 'd' and parse(code + '2') == 'b' and parse(code + '1') == 'a'

assert parse('\\def\\removedotcom#1.com{#1}\\removedotcom hello.com') == 'hello'

assert parse('\\def\\a#1at#2{(#1)(#2)}\\a helloatworld') == '(hello)(w)orld'

assert parse('\\def\\a hello{}\\a helloworld') == 'world'

assert parse('\\def\\a he#1at#2{(#1)(#2)}\\a helloatworld') == '(llo)(w)orld'

assert parse('\\def\\a#1at#2.{(#1)(#2)}\\a helloatworld.') == '(hello)(world)'

assert parse('\\def\\a#1at#2.{(#1)(#2)}\\a {hello}atworld.') == '(hello)(world)'

assert parse('\\def\\a#1at#2.{(#1)(#2)}\\a helloatw{o}{rl}d.') == '(hello)(w{o}{rl}d)'

assert parse('\\def\\a#1#2{(#1)(#2)}\\a hello') == '(h)(e)llo'
assert parse('\\def\\a#1#2{(#1)(#2)}\\a he') == '(h)(e)'

# let
assert parse('\\def\\a{hello world}\\let\\b\\a\\b') == 'hello world'


# expandafter
code = '\\def\\a#1{#1}\\def\\b#1{{hello #1}}'
assert parse(code + '\\expandafter\\a\\b{world}') == 'hello world' and parse(code + '\\a\\b{world}') == '{hello world}'


# futurelet
assert parse('\\def\\a{(\\token)}\\def\\b{hello world}\\futurelet\\token\\a\\b') == '(hello world)hello world'
