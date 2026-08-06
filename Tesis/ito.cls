%% *** Identification ***
%% The class identifies itself and the LaTeX version needed
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ito}[10/08/2022 Estilo de tesis ITO]

\newif\if@tesis
\@tesistrue
\newif\if@reporte
\@reportetrue

\DeclareOption{tesis}{\@tesistrue}
\DeclareOption{reporte}{\@reportetrue}
\ProcessOptions\relax

%% Usa como base la clase report
\LoadClass[12pt]{report}

%% *** Paquetes requeridos ***
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[letterpaper]{geometry}
\RequirePackage{amsmath,amssymb,amsthm}
\RequirePackage{newtxtext,newtxmath} % Times de alta calidad (mejor que mathptmx)
\RequirePackage{microtype}
\RequirePackage[english,spanish,mexico]{babel}
\RequirePackage{csquotes}
\RequirePackage[pagestyles,explicit]{titlesec}
\RequirePackage{titletoc}
\RequirePackage{graphicx}
\RequirePackage[table,xcdraw,dvipsnames]{xcolor}
\RequirePackage{float}
\RequirePackage[style=apa,backend=biber]{biblatex}
\RequirePackage{booktabs}
\RequirePackage{csquotes}
\RequirePackage{subfig}
\RequirePackage{enumitem}
\RequirePackage{multirow}
\RequirePackage[toc]{appendix}
\RequirePackage{pdflscape}
\RequirePackage[useregional]{datetime2}
\RequirePackage[font=bf]{caption}
\RequirePackage{newfloat}
\RequirePackage{siunitx} % Para unidades del SI
\RequirePackage[ruled,vlined,linesnumbered,spanish]{algorithm2e} % Para algoritmos
\RequirePackage[acronym,toc]{glossaries} % Para siglas y glosario

%% Define metadata pdf
\AtBeginDocument{%
  \hypersetup{%
    pdftitle={\@titulo},%
    pdfauthor={\@autor},%
    pdfsubject={Tesis doctoral},%
    pdfkeywords={\@palabras},%
    pdflang={spanish},%
    linktoc=all,%
    colorlinks=true,%
    breaklinks=true,%
    urlcolor=MidnightBlue,%
    linkcolor=MidnightBlue,%
    citecolor=DarkSlateGray%
  }%
}
\RequirePackage{hyperref}
\RequirePackage[spanish]{cleveref} % Debe ir despues de hyperref

%% *** Definicion de estilo del documento doctoral ***

%% Define float para ecuaciones

\DeclareFloatingEnvironment[
fileext=loe,
listname={\fontsize{12pt}{1pt}\selectfont LISTA DE ECUACIONES \hfill},
name=Ecuación,
within=none,
]{eq}

%% Espacio entre lineas
\linespread{1.5}

%% Fuente
% \setmainfont{Times New Roman}[
% ]

%% Tamaño de fuente para ecuaciones
\DeclareMathSizes{12}{14}{12}{10}

%% Espacio de parrafo
\setlength{\parskip}{8pt}

%% Indentacion general
\setlength{\parindent}{0pt}

%% Margenes de la pagina
\geometry{left=3.0cm,right=3.0cm,top=2.5cm,bottom=2.5cm}

%% No me acuerdo que hace uwu
\newcommand{\subfigureautorefname}{\figureautorefname}

%% Separacion de las listas
\setlist[itemize]{itemsep=3pt}

%% Separacion de las enumeraciones
\setlist[enumerate]{itemsep=3pt}

%% Traduccion de los titulos para tablas de contenido
\addto\captionsspanish{
    \renewcommand{\contentsname}%
    {\fontsize{16pt}{1pt}\selectfont CONTENIDO \hfill}%
    \renewcommand{\listfigurename}%
    {\fontsize{12pt}{1pt}\selectfont LISTA DE FIGURAS \hfill}%
  \renewcommand{\listtablename}%
  {\fontsize{12pt}{1pt}\selectfont LISTA DE TABLAS \hfill}%
  \renewcommand\appendixname{Anexo}
  \renewcommand\appendixpagename{Anexos}
  \renewcommand\appendixtocname{ANEXOS}
}

\addto\extrasspanish{%
  \renewcommand{\appendixautorefname}{Anexo}%
}

%% Definir formato de titulos de seccion
\titleformat{\chapter}{\fontsize{16pt}{1pt}\normalfont\centering}{\MakeUppercase{\chaptertitlename}
\thechapter: }{0pt}{#1}%

\titleformat{\section}{\raggedright\fontsize{14pt}{1pt}\bfseries}{\thesection}{1em}{#1}%

\titleformat{\subsection}{\raggedright\fontsize{12pt}{1pt}\bfseries}{\thesubsection}{1em}{#1}%

\titleformat{\subsubsection}{\raggedright\fontsize{12pt}{1pt}\bfseries}{\thesubsubsection}{1em}{#1}%

%% Definir espaciado de capitulo y parrafo
\titlespacing{\chapter}{0pt}{-20pt}{10pt}%

\titlespacing*{\paragraph}{0pt}{3.25ex plus 1ex minus .2ex}{0.5em}

%% Definir formato de secciones dentro de tabla de contenido
\titlecontents{chapter}% <section-type>
  [0pt]% <left>
  {}% <above-code>
  {\MakeUppercase{\@chapapp}\ \thecontentslabel: }% <numbered-entry-format>
  {}% <numberless-entry-format>
  {\titlerule*[0.3pc]{.}\contentspage}% <filler-page-format>

\titlecontents{section}% <section-type>
  [1em]% <left>
  {}% <above-code>
  {\thecontentslabel \hspace{1em}}% <numbered-entry-format>
  {}% <numberless-entry-format>
  {\titlerule*[0.3pc]{.}\contentspage}% <filler-page-format>

  \titlecontents{subsection}% <section-type>
  [2em]% <left>
  {}% <above-code>
  {\thecontentslabel \hspace{1em}}% <numbered-entry-format>
  {}% <numberless-entry-format>
  {\titlerule*[0.3pc]{.}\contentspage}% <filler-page-format>

  \titlecontents{subsubsection}% <section-type>
  [3em]% <left>
  {}% <above-code>
  {\thecontentslabel \hspace{1em}}% <numbered-entry-format>
  {}% <numberless-entry-format>
  {\titlerule*[0.3pc]{.}\contentspage}% <filler-page-format>

%% Figuras
  \titlecontents{figure}
  [0em]%
  {Figura~}
  {\vspace{-10pt}\thecontentslabel.\hspace{1em}}
  {}%
  {\titlerule*[.3pc]{.}\contentspage}%

%% Tablas
  \titlecontents{table}
  [0em]%
  {Tabla~}
  {\vspace{-10pt}\thecontentslabel.\hspace{1em}}
  {}%
  {\titlerule*[.3pc]{.}\contentspage}%

%% Ecuaciones
  \titlecontents{eq}
  [0em]%
  {Ecuación~}
  {\vspace{-10pt}\thecontentslabel.\hspace{1em}}
  {}%
  {\titlerule*[.3pc]{.}\contentspage}%

%% Apendices
  \g@addto@macro\appendices{%
    \addtocontents{toc}{\protect\renewcommand{\protect\@chapapp}{\appendixname}}%
  }

%% Enumeracion consecutiva de tablas y figuras
\counterwithout{figure}{chapter}
\counterwithout{table}{chapter}

%% Define estilo de fecha para portada
\DTMnewdatestyle{estilofecha}{%
  \renewcommand*{\DTMdisplaydate}[4]{%
    \MakeUppercase{\MYshortmonthname{##2}} ##1}%
  \renewcommand*{\DTMDisplaydate}{\DTMdisplaydate}%
}

%% Formato de titulos para preambulo
\newcommand\prechapter[1]{%
  \chapter*{#1}%
  \addcontentsline{toc}{chapter}{#1}}

%% Comando para convertir mes a texto
\newcommand{\MYshortmonthname}[1]{%
  \ifcase#1% 0
    \or Enero%
    \or Febrero%
    \or Marzo%
    \or Abril%
    \or Mayo%
    \or Junio%
    \or Julio%
    \or Agosto%
    \or Septiembre%
    \or Octubre%
    \or Noviembre%
    \or Diciembre%
  \fi
}

%% Numero de pagina a la derecha
\newpagestyle{main}{\setfoot{}{}{\thepage}}
\pagestyle{main}
\assignpagestyle{\chapter}{main}

%% Se muestra solamente hasta subseccion
\setcounter{tocdepth}{3}
\setcounter{secnumdepth}{3}

%% Remover espacio entre flotantes en distintos capitulos
\newcommand*{\noaddvspace}{\renewcommand*{\addvspace}[1]{}}
\addtocontents{lof}{\protect\noaddvspace}
\addtocontents{lot}{\protect\noaddvspace}
\addtocontents{loeq}{\protect\noaddvspace}

% \directlua{pdf.setminorversion(7)}
% \pdfminorversion=7%
% \pdfcompresslevel=0%
% \pdfobjcompresslevel=0%

%% Define la version de PDF para XeLaTeX
\special{pdf:minorversion 7} %set minorversion

%% *** Definicion de variables del documento ***
\newcommand*{\titulo}[1]{\gdef\@titulo{#1}%
}
\newcommand*{\director}[1]{\gdef\@director{#1}%
}
\newcommand*{\codirector}[1]{\gdef\@codirector{#1}%
}
\newcommand*{\autor}[1]{\gdef\@autor{#1}%
}
\newcommand*{\fecha}[1]{\gdef\@fecha{#1}%
}
\newcommand*{\keywords}[1]{\gdef\@keywords{#1}%
}
\newcommand*{\palabras}[1]{\gdef\@palabras{#1}%
}

\newcommand*{\@director}{}
\newcommand*{\@codirector}{}
\newcommand*{\@autor}{}
\newcommand*{\@fecha}{\today}
\newcommand*{\@keywords}{}
\newcommand*{\@palabras}{}

%% *** Definicion de portada ***
\renewcommand*{\maketitle}{%
\begin{titlepage}
  \begin{figure}[H]
    \centering
    \includegraphics[width=0.7\textwidth,keepaspectratio]{portada/secretaria}
  \end{figure}

  \vspace{0.5cm}

  \begin{center}
    \textbf{DIVISIÓN DE ESTUDIOS POSGRADO E INVESTIGACIÓN}
  \end{center}

  \vspace{0.2\baselineskip}
  \begin{center}
    \fontsize{11}{12}\selectfont Opción 1.- TESIS \\
    \fontsize{12}{12}\selectfont \textbf{TRABAJO PROFESIONAL}
  \end{center}

  \vspace{0.5\baselineskip}
  \centering
  \begin{minipage}{13cm}
    \begin{center}
      \fontsize{12}{12}\selectfont \textbf{\@titulo}
    \end{center}
  \end{minipage}


  \vspace{0.5\baselineskip}
  \begin{center}
    \fontsize{11}{12}\selectfont \textbf{QUE PARA OBTENER EL GRADO DE:} \\
    \fontsize{12}{12}\selectfont \textbf{DOCTOR EN CIENCIAS} \\
    \fontsize{12}{12}\selectfont \textbf{DE LA INGENIERÍA}
  \end{center}

  \vspace{0.5\baselineskip}
  \begin{center}
    \fontsize{11}{12}\selectfont \textbf{PRESENTA:} \\
    \fontsize{12}{12}\selectfont \@autor
  \end{center}

  \vspace{1\baselineskip}
  \begin{center}
    \fontsize{11}{12}\selectfont \textbf{DIRECTOR DE TESIS:} \\
    \fontsize{12}{12}\selectfont \@director
  \end{center}

  \ifx\@codirector\empty
  \else
    \vspace{1\baselineskip}
    \begin{center}
        \fontsize{11}{12}\selectfont \textbf{CODIRECTOR DE TESIS:} \\
        \fontsize{12}{12}\selectfont \@codirector
    \end{center}
  \fi

 \vspace{2\baselineskip}
\noindent
 \begin{minipage}[t]{.2\textwidth}
\raggedleft
    \includegraphics[width=2.5cm,keepaspectratio]{portada/ito_logo}
\end{minipage}%
\begin{minipage}[t]{.8\textwidth}
    \vspace{1cm}
    \fontsize{10}{12}\selectfont \hfill CHIHUAHUA, CHIHUAHUA, MÉXICO \hfill \DTMsetdatestyle{estilofecha}\@fecha
\end{minipage}

\end{titlepage}

}

\makeatletter

\patchcmd{\@setref}{\bfseries??}{\colorbox{red!30}{\detokenize{#3}}}{}{}

\ifdefined\HyRef@autosetref\patchcmd{\HyRef@autosetref}
      {\else}{\else\colorbox{red!30}{\detokenize{#2}}}{}{}\fi

\def\abx@missing#1{\colorbox{red!30}{\detokenize{#1}}}

\makeatother
