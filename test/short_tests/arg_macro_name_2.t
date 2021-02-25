\def{1}{a}
\def{2}{c}
\def{a}{\1{}b\2{}}
\def{c}{a}
\def{1abc}{mmm}
\1abc{}
\def{wrap}{\2#bc{}}
\a{}


\wrap{\ifdef{hello}{1}{2}}
