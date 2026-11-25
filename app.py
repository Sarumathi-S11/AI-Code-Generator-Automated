import streamlit as st
from code_generator import AICodeGenerator
st.set_page_config(page_title='AI Code Generator',page_icon='🤖',layout='wide')
g=AICodeGenerator()
st.title('🤖 AI Code Generator Automated')
st.caption('Generate starter code from plain-English descriptions using NLP patterns and Jinja2 templates.')
with st.sidebar:
 language=st.selectbox('Programming language',['python','javascript','java'])
 stats=g.statistics(); st.metric('Saved generations',stats['total']); st.metric('Valid outputs',f"{stats['valid_percentage']}%")
t1,t2,t3=st.tabs(['Code Generator','Snippet Library','History & Stats'])
with t1:
 prompt=st.text_area('Describe the code you need',placeholder='Create a function called calculate_sum with parameters a, b',height=110)
 if st.button('Generate code',type='primary'):
  st.session_state.result=g.generate_code(prompt,language) if prompt.strip() else {'success':False,'error':'Please enter a description.'}
 result=st.session_state.get('result')
 if result:
  if result['success']:
   a,b=st.columns([3,1])
   with a:
    st.subheader('Generated code'); st.code(result['code'],language=language)
    ext={'python':'py','javascript':'js','java':'java'}[language]
    st.download_button('Download source file',result['code'],f'generated_code.{ext}')
   with b:
    st.write('**Intent:**',result['intent']); st.write('**Name:**',result['metadata']['name']); st.write('**Parameters:**',', '.join(result['metadata']['parameters']) or 'None')
    (st.success if result['validation']['valid'] else st.error)(result['validation']['message'])
   st.subheader('Code explanation'); st.write(g.explain_code(result['code'],language))
   if language=='python':
    with st.expander('Unit-test starter'):
     tests=g.generate_unit_test(result['code']); st.code(tests,language='python'); st.download_button('Download tests',tests,'test_generated_code.py')
  else:
   st.error(result['error'])
   for x in result.get('suggestions',[]): st.markdown('- '+x)
with t2:
 st.subheader('Ready-made prompt library')
 for label,prompt in [('Function','Create a function called calculate_sum with parameters a, b'),('Class','Create a class called Student with parameters name, age'),('Loop','Write a loop over items'),('Sort','Sort a list'),('Search','Create a search function')]:
  with st.expander(label): st.code(prompt)
with t3:
 st.subheader('Generation history')
 if g.history: st.dataframe(list(reversed(g.history[-30:])),use_container_width=True,hide_index=True)
 else: st.info('No generations yet. Try the generator first.')
 st.json(g.statistics())
