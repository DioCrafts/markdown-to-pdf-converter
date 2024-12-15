# Markdown to PDF Filter

## 🚀 Overview

**Markdown to PDF Filter** es un filtro para **Pandoc** que convierte archivos **Markdown** en documentos **PDF**, con soporte para:

- 📝 **Bloques de código**: Resaltado de sintaxis con el paquete `listings` de LaTeX.
- 📊 **Diagramas Mermaid**: Genera diagramas a partir de código Mermaid.
- 🌱 **Diagramas PlantUML**: Renderiza diagramas UML definidos con PlantUML.

Perfecto para generar documentación técnica automatizada con un estilo profesional.

---

## 📦 Requirements

1. **Python** >= 3.8
2. **Pandoc** >= 2.11
3. **Mermaid CLI** (mmdc): [Instalación](https://github.com/mermaid-js/mermaid-cli)
4. **PlantUML**: [Instalación](https://plantuml.com/starting)
5. LaTeX: Necesario para generar el PDF (Ej. [TeX Live](https://tug.org/texlive/))

---

## 🛠️ Installation

Clona el repositorio y asegúrate de instalar los requisitos:

```bash
git clone https://github.com/yourusername/markdown-to-pdf-filter.git
cd markdown-to-pdf-filter
pip install panflute
```

---

## 💡 Usage

### 1. Estructura del archivo Markdown

Crea tu archivo Markdown (`example.md`) con bloques Mermaid y PlantUML:

```markdown
## Ejemplo de Código

\`\`\`python
def hello_world():
    print("Hello, World!")
\`\`\`

### Ejemplo de Diagrama Mermaid

\`\`\`mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
\`\`\`

### Ejemplo de PlantUML

\`\`\`plantuml
@startuml
Alice -> Bob: Hola Bob
@enduml
\`\`\`
```

### 2. Ejecuta Pandoc con el filtro

```bash
pandoc -F ./pandoc_filter.py -o output.pdf example.md
```

---

## 🎨 Features

- **Soporte completo para Mermaid** y **PlantUML**.
- Formateo elegante de bloques de código usando LaTeX `listings`.
- Espaciado automático entre títulos y bloques de código.
- Configuración personalizable (colores, márgenes, grosor del borde).

---

## 📚 Dependencies

- `panflute`
- `pandoc`
- `mmdc` (Mermaid CLI)
- `plantuml`

Instalación rápida de Python dependencies:
```bash
pip install panflute
```

---

## 🖼️ Ejemplo de salida

Ejecutar el filtro genera un **PDF** limpio y profesional con diagramas renderizados.

---

## 🤝 Contributing

¡Las contribuciones son bienvenidas! Abre un **issue** o envía un **pull request**.

---

## 📜 License

Este proyecto está licenciado bajo **MIT License**.

---

## 🔍 SEO Keywords

Markdown to PDF, Pandoc Filter, Mermaid Diagrams, PlantUML Support, Code Blocks to PDF, Convert Markdown to PDF, Pandoc Mermaid Integration, Technical Documentation Generator.
