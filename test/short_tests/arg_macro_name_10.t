\def{hello}{\def{12#45}{abcd#}}

\hello{}

\ifdef{1245}{1}{2}

\undef{1245}

\hello{3}

\ifdef{12345}{1}{2}
\12345{}
\12345{6}
\undef{12345}
