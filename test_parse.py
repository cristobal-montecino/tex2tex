from parse import parse

assert parse('\\def\\newcommand#1#2{\\def#1{#2}}\\newcommand{\\hello}{hello world}\\hello world') == 'hello worldworld'

assert parse('\\def\\eat#1{}\eat hello') == 'ello'

assert parse('\\def\\parse user: #1, number: #2{Hello #1 (###2)}\\parse user: {John}, number: {1}') == 'Hello John (#1)'
