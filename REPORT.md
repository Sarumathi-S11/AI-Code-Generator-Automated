# AI Code Generator Automated — Project Report

**Task ID:** AI-SD-001 | **Student Code:** DAS012952

## Objective
Build a system that converts plain-English programming requests into starter code and validates generated source structure.

## Technologies
Python, regular expressions for lightweight NLP intent detection, Jinja2 for template rendering, Python AST for syntax validation, Streamlit for the user interface, JSON for history and pytest for testing.

## Methodology
The input prompt is normalized and matched against intent patterns for functions, classes, loops, sorting and searching. The system extracts names and parameters, selects a language-specific Jinja2 template and renders code for Python, JavaScript or Java. Python output is parsed with `ast.parse`; the other languages receive a basic bracket/string structural check. The generation metadata and validation result are saved in JSON.

## Features
Natural-language input, intent recognition, multi-language template output, Python AST validation, code explanation, unit-test starter generation, snippet library, generation history, statistics, Streamlit UI and source download.

## Testing
Automated tests cover function and class generation, JavaScript output, unknown-intent handling, explanation and unit-test starter generation. Run `pytest -q` from the project folder.

## Conclusion
The project demonstrates a working template-based code-generation workflow. It is an educational prototype, not a full generative language model. Transformer integration and language-specific compiler validation are suitable future improvements.

## Evidence to attach
Add screenshots of the UI, generated code in multiple languages, validation/explanation and history. Add public GitHub and YouTube URLs to README before submission.
