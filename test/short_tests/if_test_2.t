\def{hello}{#}
\def{m}{\if{\hello{#}}{1}{2}}


\m{}
\m{1}

\def{n}{\if{#}{1}{2}}

\n{1}
\n{}
\n{\hello{}}
\n{\hello{1}}
