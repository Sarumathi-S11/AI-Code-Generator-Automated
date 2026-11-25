import ast, json, re
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, BaseLoader

ROOT = Path(__file__).parent
HISTORY = ROOT / 'data' / 'generation_history.json'
TEMPLATES = {
 'python': {
  'function': 'def {{ name }}({{ params }}):\n    """{{ description }}"""\n    # TODO: Add implementation\n    pass\n',
  'class': 'class {{ name }}:\n    """{{ description }}"""\n\n    def __init__(self{% for p in param_list %}, {{ p }}{% endfor %}):\n{% if param_list %}{% for p in param_list %}        self.{{ p }} = {{ p }}\n{% endfor %}{% else %}        pass\n{% endif %}',
  'loop': 'for item in {{ iterable }}:\n    print(item)\n',
  'sort': 'def sort_list(values):\n    """Return values sorted in ascending order."""\n    return sorted(values)\n',
  'search': 'def linear_search(values, target):\n    """Return target index, or -1 when absent."""\n    for index, value in enumerate(values):\n        if value == target:\n            return index\n    return -1\n'},
 'javascript': {
  'function': 'function {{ name }}({{ params }}) {\n    // {{ description }}\n    // TODO: Add implementation\n}\n',
  'class': 'class {{ name }} {\n    constructor({{ params }}) {\n{% for p in param_list %}        this.{{ p }} = {{ p }};\n{% endfor %}    }\n}\n',
  'loop': 'for (const item of {{ iterable }}) {\n    console.log(item);\n}\n',
  'sort': 'function sortList(values) { return [...values].sort((a, b) => a - b); }\n',
  'search': 'function linearSearch(values, target) {\n    for (let i = 0; i < values.length; i++) { if (values[i] === target) return i; }\n    return -1;\n}\n'},
 'java': {
  'function': 'public static Object {{ name }}({{ java_params }}) {\n    // {{ description }}\n    // TODO: Add implementation\n    return null;\n}\n',
  'class': 'public class {{ name }} {\n{% for p in param_list %}    private Object {{ p }};\n{% endfor %}    public {{ name }}({{ java_params }}) {\n{% for p in param_list %}        this.{{ p }} = {{ p }};\n{% endfor %}    }\n}\n',
  'loop': 'for (Object item : {{ iterable }}) { System.out.println(item); }\n',
  'sort': 'import java.util.Arrays;\npublic class SortExample { public static int[] sortArray(int[] values) { int[] copy = values.clone(); Arrays.sort(copy); return copy; } }\n',
  'search': 'public static int linearSearch(int[] values, int target) { for (int i=0; i<values.length; i++) { if (values[i]==target) return i; } return -1; }\n'}
}

class AICodeGenerator:
 def __init__(self):
  self.env = Environment(loader=BaseLoader())
  try: self.history = json.loads(HISTORY.read_text(encoding='utf-8'))
  except (FileNotFoundError, json.JSONDecodeError): self.history = []
  self.patterns = {'function':r'\b(function|method|def)\b','class':r'\b(class|object)\b','loop':r'\b(loop|iterate|for each)\b','sort':r'\b(sort|sorting|order)\b','search':r'\b(search|find|lookup)\b'}

 def detect_intent(self, text):
  text = re.sub(r'\s+', ' ', text.lower().strip())
  for intent, pattern in self.patterns.items():
   if re.search(pattern, text): return intent
  return 'unknown'

 def extract_name(self, text, intent):
  pats = {'function':[r'(?:function|method)\s+(?:called|named)?\s*([A-Za-z_]\w*)',r'\bdef\s+([A-Za-z_]\w*)'], 'class':[r'class\s+(?:called|named)?\s*([A-Za-z_]\w*)']}
  for p in pats.get(intent, []):
   m = re.search(p, text, re.I)
   if m: return m.group(1)
  return 'my_function' if intent == 'function' else 'MyClass'

 def extract_params(self, text):
  m = re.search(r'\(([^()]*)\)', text)
  if not m: m = re.search(r'(?:parameters?|arguments?|args?)\s+([A-Za-z_,\s]+)', text, re.I)
  if not m: return []
  return list(dict.fromkeys(x.strip() for x in m.group(1).split(',') if re.fullmatch(r'[A-Za-z_]\w*', x.strip())))

 def validate_code(self, code, language='python'):
  if language == 'python':
   try: ast.parse(code); return {'valid':True,'message':'Python syntax is valid.'}
   except SyntaxError as e: return {'valid':False,'message':f'Syntax error: {e.msg}','line':e.lineno}
  pairs = {')':'(',']':'[','}':'{'}; stack=[]; quote=None; escape=False
  for ch in code:
   if quote:
    if escape: escape=False
    elif ch == '\\': escape=True
    elif ch == quote: quote=None
   elif ch in "'\"`": quote=ch
   elif ch in '([{': stack.append(ch)
   elif ch in ')]}':
    if not stack or stack.pop()!=pairs[ch]: return {'valid':False,'message':'Mismatched brackets.'}
  ok = not stack and quote is None
  return {'valid':ok,'message':'Basic structure check passed.' if ok else 'Unclosed bracket or string.'}

 def generate_code(self, description, language='python'):
  if language not in TEMPLATES: return {'success':False,'error':'Choose Python, JavaScript or Java.'}
  intent=self.detect_intent(description)
  if intent=='unknown': return {'success':False,'error':'Could not identify the code request. Try a function, class, loop, sort or search request.','suggestions':['Create a function called calculate_sum with parameters a, b','Create a class called Student with parameters name, age','Write a loop over items','Sort a list','Create a search function']}
  name=self.extract_name(description,intent); params=self.extract_params(description)
  iterable_match=re.search(r'(?:over|through|in)\s+(?:the\s+)?([A-Za-z_]\w*)',description,re.I)
  iterable=iterable_match.group(1) if iterable_match else 'items'
  template=self.env.from_string(TEMPLATES[language][intent])
  code=template.render(name=name,params=', '.join(params),param_list=params,java_params=', '.join('Object '+p for p in params),description=description.replace('"""',"'''"),iterable=iterable).rstrip()+'\n'
  validation=self.validate_code(code,language)
  result={'success':True,'code':code,'intent':intent,'language':language,'metadata':{'name':name,'parameters':params},'validation':validation}
  self.history.append({'timestamp':datetime.now().isoformat(timespec='seconds'),'description':description,'intent':intent,'language':language,'valid':validation['valid']})
  HISTORY.parent.mkdir(parents=True,exist_ok=True); HISTORY.write_text(json.dumps(self.history[-100:],indent=2),encoding='utf-8')
  return result

 def explain_code(self, code, language='python'):
  if language!='python': return 'Review the generated language-specific code and its comments.'
  try: tree=ast.parse(code)
  except SyntaxError as e: return f'Cannot explain invalid syntax: {e.msg}'
  notes=[]
  for n in ast.walk(tree):
   if isinstance(n,ast.FunctionDef): notes.append(f"Function {n.name}: parameters {', '.join(a.arg for a in n.args.args) or 'none'}.")
   elif isinstance(n,ast.ClassDef): notes.append(f'Class {n.name}: an object blueprint.')
   elif isinstance(n,ast.For): notes.append('For-loop: repeats a block for each item.')
   elif isinstance(n,ast.If): notes.append('If-statement: executes code when a condition is true.')
  return '\n'.join(dict.fromkeys(notes)) or 'No major Python constructs detected.'

 def generate_unit_test(self, code):
  try: tree=ast.parse(code)
  except SyntaxError: return '# Cannot generate tests: Python syntax is invalid.\n'
  funcs=[n.name for n in tree.body if isinstance(n,ast.FunctionDef)]
  if not funcs: return '# No top-level functions found.\n'
  lines=['import unittest','','class GeneratedTests(unittest.TestCase):']
  for f in funcs: lines += [f'    def test_{f}_placeholder(self):',f'        # TODO: Add meaningful assertions for {f}.','        self.assertTrue(callable('+f+'))','']
  return '\n'.join(lines)+'\nif __name__ == "__main__":\n    unittest.main()\n'

 def statistics(self):
  total=len(self.history); valid=sum(bool(x.get('valid')) for x in self.history); by={}
  for x in self.history: by[x['intent']]=by.get(x['intent'],0)+1
  return {'total':total,'valid':valid,'valid_percentage':round(valid*100/total,1) if total else 0,'by_intent':by}
