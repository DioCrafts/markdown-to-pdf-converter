# Markdown to PDF Filter

## 🚀 Overview

**Markdown to PDF Filter** is a **Pandoc** filter that converts **Markdown** files into **PDF** documents, with support for:

- 📝 **Code blocks**: Syntax highlighting using the LaTeX `listings` package.
- 📊 **Mermaid diagrams**: Generates diagrams from Mermaid code.
- 🌱 **PlantUML diagrams**: Renders UML diagrams defined with PlantUML.

Perfect for generating automated technical documentation with a professional style.

---

## 📦 Requirements

1. **Python** >= 3.8
2. **Pandoc** >= 2.11
3. **Mermaid CLI** (mmdc): [Installation](https://github.com/mermaid-js/mermaid-cli)
4. **PlantUML**: [Installation](https://plantuml.com/starting)
5. LaTeX: Required for PDF generation (e.g., [TeX Live](https://tug.org/texlive/))

---

## 🛠️ Installation

Clone the repository and make sure to install the requirements:

```bash
git clone https://github.com/yourusername/markdown-to-pdf-filter.git
cd markdown-to-pdf-filter
pip install -r requirements.txt
```

---

## 💡 Usage

### 1. Markdown file structure

Create your Markdown file (`example.md`) with Mermaid and PlantUML blocks:

```markdown
## Code Example

\`\`\`python
def hello_world():
    print("Hello, World!")
\`\`\`

### Mermaid Diagram Example

\`\`\`mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
\`\`\`

### PlantUML Example

\`\`\`plantuml
@startuml
Alice -> Bob: Hello Bob
@enduml
\`\`\`
```

### 2. Run Pandoc with the filter

```bash
pandoc -F ./markdown-to-pdf-convert.py -o output.pdf example.md
```

### 3. Markdown file inclusion (mdinclude)

You can include other Markdown files within your document:

\`\`\`mdinclude
./docs/intro.md
./docs/chapter1.md
# This line is a comment and will be ignored
Increase_headers=True
./docs/appendix.md
\`\`\`

**Options:**
- `Increase_headers=True`: Increases the header level of the included file
- Lines starting with `#` are ignored as comments

### 4. Code inclusion from files (codeblock-include)

Include content from external files in a code block:

\`\`\`codeblock-include
./src/example.py
./src/utils.py
\`\`\`

---

## 🎨 Features

- **Full support for Mermaid** and **PlantUML**.
- Elegant code block formatting using LaTeX `listings`.
- Automatic spacing between headers and code blocks.
- Customizable configuration (colors, margins, border thickness).

---

## 📚 Dependencies

- `panflute`
- `pandoc`
- `mmdc` (Mermaid CLI)
- `plantuml`

Quick Python dependencies installation:
```bash
pip install -r requirements.txt
```

---

## 🖼️ Output Example

Running the filter generates a **clean and professional PDF** with rendered diagrams.

---

## 🤝 Contributing

Contributions are welcome! Open an **issue** or submit a **pull request**.

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

---

## 🔍 SEO Keywords

Markdown to PDF, Pandoc Filter, Mermaid Diagrams, PlantUML Support, Code Blocks to PDF, Convert Markdown to PDF, Pandoc Mermaid Integration, Technical Documentation Generator.
