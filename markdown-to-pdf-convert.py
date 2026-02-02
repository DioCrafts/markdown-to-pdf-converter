#!/usr/bin/env python3

"""
Pandoc filter using panflute for PlantUML and Mermaid
"""

import hashlib
import sys
import os
import re
import subprocess
import panflute as pf

PLANTUML_BIN = os.environ.get('PLANTUML_BIN', 'plantuml')
MERMAID_BIN = os.path.expanduser(os.environ.get('MERMAID_BIN', 'mmdc'))

def prepare(doc):
    if doc.format in ['latex', 'pdf']:
        doc.metadata['header-includes'] = [
            pf.RawBlock(r'\usepackage[utf8]{inputenc}', format="latex"),
            pf.RawBlock(r'\usepackage[T1]{fontenc}', format="latex"),
            pf.RawBlock(r'\usepackage{textcomp}', format="latex"),
            pf.RawBlock(r'\usepackage{graphicx}', format="latex"),
            pf.RawBlock(r'\usepackage{caption}', format="latex"),
            pf.RawBlock(r'\usepackage{float}', format="latex"),
            pf.RawBlock(r'\usepackage{listings}', format="latex"),
            pf.RawBlock(r'\usepackage{capt-of}', format="latex"),
            pf.RawBlock(r'\usepackage{xcolor}', format="latex"),
            pf.RawBlock(r'\usepackage[a4paper, top=3cm, bottom=3cm, left=2.5cm, right=2.5cm]{geometry}', format="latex"),
            pf.RawBlock(r"""
% Define custom colors
\definecolor{background}{RGB}{250, 251, 254}
\definecolor{keyword}{RGB}{0, 0, 255}        % blue for keywords
\definecolor{identifier}{RGB}{0, 0, 0}       % black for identifiers
\definecolor{comment}{RGB}{58, 127, 179}     % blue-ish for comments
\definecolor{string}{RGB}{163, 21, 21}       % dark red for strings
\definecolor{border}{RGB}{230, 230, 230}     % light gray for border

\lstset{
    basicstyle=\ttfamily\small\color{identifier},
    keywordstyle=\color{keyword},
    commentstyle=\itshape\color{comment},
    stringstyle=\color{string},
    showstringspaces=false,
    breaklines=true,
    frame=single,
    framerule=0.1pt,
    rulecolor=\color{border},
    backgroundcolor=\color{background},
    numbers=none,
    numberstyle=\tiny\color{gray},
    stepnumber=1,
    tabsize=4,
    aboveskip=10pt,
    belowskip=10pt,
    framexleftmargin=5pt,
    framexrightmargin=5pt,
    framexbottommargin=4pt,
    framextopmargin=4pt,
    frameround=tttt,
    abovecaptionskip=25pt,
    captionpos=t,
    floatplacement=t,
    float=t,
    literate={á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1
             {Á}{{\'A}}1 {É}{{\'E}}1 {Í}{{\'I}}1 {Ó}{{\'O}}1 {Ú}{{\'U}}1
             {ñ}{{\~n}}1 {Ñ}{{\~N}}1 {ü}{{\"u}}1 {Ü}{{\"U}}1
}
""", format="latex")
        ]

def finalize(doc):
    pass

def process_mermaid(elem, doc):
    """Render mermaid diagrams and force exact position in LaTeX."""
    if isinstance(elem, pf.CodeBlock) and 'mermaid' in elem.classes:
        filename = get_filename4code("mermaid", elem.text)
        filetype = get_extension(doc.format, "png", html="svg", latex="png")

        src = filename + '.mmd'
        dest = filename + '.' + filetype

        if not os.path.isfile(dest):
            txt = elem.text.encode(sys.getfilesystemencoding())
            with open(src, "wb") as f:
                f.write(txt)

        # Generate the diagram
        cmd = [MERMAID_BIN, "-i", src, "-o", dest, "--scale", "4"]
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            pf.debug(f'Error generating Mermaid diagram: {e}\n')
            return None

        # Use the H option to prevent floating
        if doc.format in ['latex', 'pdf']:
            latex_code = rf"""
\noindent
\begin{{figure}}[H]
    \centering
    \includegraphics[width=\textwidth]{{{dest}}}
    \caption{{Mermaid diagram}}
\end{{figure}}
"""
            return pf.RawBlock(latex_code, format="latex")

        return pf.Para(pf.Image(url=dest))


def process_plantuml(elem, doc):
    """Render PlantUML diagrams and format the output for LaTeX."""
    if isinstance(elem, pf.CodeBlock) and 'plantuml' in elem.classes:
        filename = get_filename4code("plantuml", elem.text)
        filetype = get_extension(doc.format, "png", html="svg", latex="png")

        src = filename + '.uml'
        dest = filename + '.' + filetype

        if not os.path.isfile(dest):
            txt = elem.text.encode(sys.getfilesystemencoding())
            if not txt.startswith(b"@start"):
                txt = b"@startuml\n" + txt + b"\n@enduml\n"
            with open(src, "wb") as f:
                f.write(txt)

        subprocess.check_call(PLANTUML_BIN.split() + ["-t" + filetype, src])

        # For LaTeX output, ensure full-width scaling
        if doc.format in ['latex', 'pdf']:
            latex_code = rf"""
\begin{{figure}}[htbp]
    \centering
    \includegraphics[width=\textwidth]{{{dest}}}
    \caption{{PlantUML diagram}}
\end{{figure}}
"""
            return pf.RawBlock(latex_code, format="latex")

        return pf.Para(pf.Image(url=dest))



def process_codeblocks(elem, doc):
    """
    Format code blocks using the 'listings' package for LaTeX output,
    excluding Mermaid blocks.
    """
    if isinstance(elem, pf.CodeBlock):
        # Skip Mermaid blocks
        if 'mermaid' in elem.classes:
            return None

        if doc.format in ['latex', 'pdf']:
            # Detect language
            language = elem.classes[0] if elem.classes else "text"

            # Supported languages
            supported_languages = [
                "python", "java", "c", "cpp", "javascript", "bash", "html",
                "xml", "sql", "json", "yaml", "go", "ruby", "perl", "text"
            ]
            language_option = f"[language={language}]" if language in supported_languages else ""

            # Normalize the text to avoid encoding issues
            normalized_text = elem.text.encode("utf-8", errors="replace").decode("utf-8")

            # Generate the LaTeX block with \noindent and custom spacing
            latex_code = rf"""
\vspace{{5pt}}
\noindent
\begin{{lstlisting}}{language_option}
{normalized_text}
\end{{lstlisting}}
"""
            return pf.RawBlock(latex_code, format="latex")

        return elem




def process_codeblockinclude(elem, doc):
    """Change Text in codeblock from an included
    file that is placed in the codeblock

    Arguments:
    elem -- The element that should be processed
    doc  -- The document
    """

    if isinstance(elem, pf.CodeBlock) and 'codeblock-include' in elem.classes:
        concatinated_file_content = ''

        # Within the codeblock the files are listed. We extract them
        file_names = elem.text.splitlines()
        for c, file_name in enumerate(file_names):
            if not file_name.startswith('#'):
                try:
                    file_content = open(file_name, "r", encoding="utf-8")
                    concatinated_file_content = concatinated_file_content + file_content.read()
                except (FileNotFoundError, IOError, PermissionError) as e:
                    pf.debug(f'Error reading {file_name}: {e}\n')

        elem.text = concatinated_file_content
    return None


def get_filename4code(module, content, ext=None):
    """Generate filename based on content."""
    imagedir = module + "-images"
    fn = hashlib.sha1(content.encode(sys.getfilesystemencoding())).hexdigest()
    try:
        os.mkdir(imagedir)
        sys.stderr.write('Created directory ' + imagedir + '\n')
    except OSError:
        pass
    if ext:
        fn += "." + ext
    return os.path.join(imagedir, fn)

def get_extension(format, default, **alternates):
    """Get file extension for the result."""
    return alternates.get(format, default)


# Global variable for tracking included file directory (used by change_uri)
dirname_of_included_mdfile = "./"


def process_mdinclude(elem, doc):
    """Recursive mdinclude based on mdinclude CodeBlock

    Arguments:
    elem -- The element that should be processed
    doc  -- The document
    """

    if isinstance(elem, pf.CodeBlock) and 'mdinclude' in elem.classes:
        # We take the received element and turn it into a list of elements
        # that are derived from the included markdown file
        list_of_converted_elements = convert_code_element_to_list_of_elements(
            elem, doc)

        # Enumerate over the new elements and see if there are
        # further mdinclude codeblocks to include
        # Since enumerate is also working over a list that is changed
        # during enumeration this works in a recursive manner
        for n, element in enumerate(list_of_converted_elements):

            # There seems to be one
            if isinstance(element, pf.CodeBlock) and 'mdinclude' in element.classes:
                # Convert it
                next_converted_list = convert_code_element_to_list_of_elements(
                    element, doc)
                # Remove the codeblock
                del list_of_converted_elements[n]
                # Insert the new elements at the place
                # Where the codeblock was
                list_of_converted_elements[n:n] = next_converted_list

        return list_of_converted_elements
    pass


def convert_code_element_to_list_of_elements(elem, doc):
    """Conversion of a codeblock element to a list of elements
    that have been extracted from the included markdown

    Ignores lines with # as comments
    Honors the following control keywords:
        Increase_headers=True -- If set headers in the included files are
                                 increased by one level

    Arguments:
    elem -- The element that should be processed
    doc  -- The document

    Returns a list with the converted elements
    """

    # Safety first. In case we use this function for a recursive call.
    # If Not, we can remove it anyway
    if isinstance(elem, pf.CodeBlock) and 'mdinclude' in elem.classes:
        # All files in one codeblock will be combined as if they
        # where one file. We need a string to concatinate the file_content
        # of all files
        concatinated_file_content = ''
        increase_headers = False

        included_elements = []

        # Within the codeblock the files are listed. We extract them
        file_names = elem.text.splitlines()
        for c, file_name in enumerate(file_names):
            if 'Increase_headers=True' in file_name:
                increase_headers = True
                continue

            if 'Increase_headers=False' in file_name:
                continue

            if not file_name.startswith('#') and file_name.strip():
                try:
                    # extracting the directory name for later use
                    # in case we need to change the image URI
                    global dirname_of_included_mdfile
                    dirname_of_included_mdfile = os.path.dirname(
                        file_name) + '/'

                    if dirname_of_included_mdfile == "/" or dirname_of_included_mdfile == "":
                        dirname_of_included_mdfile = "./"

                    # Read the file and store as string
                    content_as_string = open(
                        file_name, "r", encoding="utf-8").read()

                    # Convert all to pandoc elements and add them
                    # to the list of elements
                    content_as_elements = pf.convert_text(content_as_string)

                    # Test recursion
                    for n, element in enumerate(content_as_elements):
                        element.walk(change_uri, doc=None)

                    included_elements.extend(content_as_elements)
                except (FileNotFoundError, IOError, PermissionError) as e:
                    pf.debug(f'Error reading {file_name}: {e}\n')

        # User want to increase the header levels
        if increase_headers:
            for n, element in enumerate(included_elements):
                if isinstance(element, pf.Header):
                    element.level += 1
                    included_elements[n] = element

        return included_elements

    # Just in case it is no Codeblock we pass through
    pass


def change_uri(elem, doc):
    """Private Helper that is called in mdinclude parser to change
    relative URIs

    Arguments:
    elem -- The element that should be processed
    doc  -- The document
    """

    if isinstance(elem, pf.Image):
        # In case we found an Image we need to change the URI
        # based on the location the file that is including the
        # image. We do this by prepending the global variable
        new_url = dirname_of_included_mdfile + elem.url
        elem.url = new_url
    if isinstance(elem, pf.CodeBlock) and 'mdinclude' in elem.classes:
        # More or less the same thing for other mdincludes. But in
        # this case we change the element text after all URIs have been
        # rewritten.
        file_names = elem.text.splitlines()
        for c, file_name in enumerate(file_names):
            if 'Increase_headers' in file_name:
                continue
            if not file_name.startswith('#') and file_name.strip():
                new_file_name = dirname_of_included_mdfile + file_name
                file_names[c] = new_file_name
        new_text = '\n'.join(file_names)
        elem.text = new_text
    pass


def add_spacing_after_headers(elem, doc):
    """
    Añade \vspace{5pt} después de los encabezados de nivel 4 (####).
    """
    if isinstance(elem, pf.Header) and elem.level == 4:
        return [elem, pf.RawBlock(r'\vspace{5pt}', format="latex")]

def main(doc=None):
    """Run the filters."""
    return pf.run_filters(
        [
            process_mdinclude,
            process_codeblockinclude,
            process_codeblocks,
            process_mermaid,
            process_plantuml,
            add_spacing_after_headers
        ],
        prepare=prepare,
        finalize=finalize,
        doc=doc
    )


if __name__ == '__main__':
    main()
