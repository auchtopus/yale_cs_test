\def{hello}{\def{#}{mn}}



\def{m}{\if{#}{x}{2}}


\m{}
\m{\ifdef{bye}{}{2}}
\m{\ifdef{hello}{}{2}}
\ifdef{bye}{}{2}
\ifdef{hello}{}{2}



\m{\include{empty.in}}
