from code_generator import AICodeGenerator

def test_function_generation_and_ast():
 r=AICodeGenerator().generate_code('Create a function called calculate_sum with parameters a, b')
 assert r['success'] and r['validation']['valid'] and 'def calculate_sum(a, b)' in r['code']

def test_class_generation():
 r=AICodeGenerator().generate_code('Create a class called Student with parameters name, age')
 assert r['success'] and r['validation']['valid'] and 'class Student' in r['code']

def test_javascript_generation():
 r=AICodeGenerator().generate_code('Sort a list','javascript')
 assert r['success'] and r['validation']['valid'] and 'function sortList' in r['code']

def test_unknown_intent():
 r=AICodeGenerator().generate_code('Make something nice')
 assert not r['success'] and r['suggestions']

def test_explanation_and_unit_test():
 g=AICodeGenerator(); r=g.generate_code('Create a function called greet with parameters name')
 assert 'greet' in g.explain_code(r['code']) and 'test_greet' in g.generate_unit_test(r['code'])
