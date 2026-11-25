# AI Code Generator Automated

**Task ID:** AI-SD-001  
**Domain:** Software Development Assistance  
**Student Code:** DAS012952  
**Company:** Data Alcott Systems

A natural-language-to-code educational assistant using Python, NLP-style intent recognition, Jinja2 templates and code validation.

## Features
- Plain-English input preprocessing and keyword/regex intent recognition
- Function, class, loop, sorting and searching code generation
- Python, JavaScript and Java templates
- Jinja2 template rendering
- Python AST syntax validation; basic bracket/string checks for JS and Java
- Python code explanation and unit-test starter generation
- JSON generation history, statistics and Streamlit interface
- Snippet prompt library and source-file download

## Stack
Python, regular expressions, Jinja2, AST, Streamlit, JSON, pytest. NLTK is included as an optional dependency for further NLP experimentation; the current implementation uses lightweight regex preprocessing and does not download language corpora.

## Run on Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again. Open the localhost URL printed in the terminal (usually http://localhost:8501).

## Tests
```powershell
pytest -q
```

## Example prompts
- Create a function called calculate_sum with parameters a, b
- Create a class called Student with parameters name, age
- Write a loop over items
- Sort a list
- Create a search function

## Workflow
1. Normalize the natural-language prompt.
2. Detect intent with keyword and regular-expression patterns.
3. Extract function/class name and parameters.
4. Render a language-specific Jinja2 template.
5. Validate Python with `ast.parse`; apply a lightweight structural check to JavaScript/Java.
6. Save generation metadata and validation status in JSON history.

## Limitations
This is a template-driven prototype, not a trained large language model. It supports a limited set of code intents. AST validation is applied to Python only; JavaScript/Java checks are structural and are not compiler validation. Generated code is starter code and must be reviewed and tested before real use.

## Submission links
- GitHub: `ADD_YOUR_GITHUB_REPOSITORY_URL`
- YouTube demo: `ADD_YOUR_YOUTUBE_VIDEO_URL`

## Screenshots to capture
1. Generator home and natural-language input
2. Python function output
3. Class or loop output
4. JavaScript/Java output
5. Validation, explanation and test starter
6. History/statistics page

## Future work
Integrate a transformer-based code model, language-specific parsers/compilers, semantic intent classification, custom templates and more meaningful generated unit tests.
