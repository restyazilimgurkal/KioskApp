import configparser
import os
import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import get_page_location
from streamlit_extras.switch_page_button import switch_page
import math

def load_configuration():
    """
    Function to load the configuration settings from 'config.ini'.
    If the configuration has been loaded before, it is stored in the session state to avoid reloading.
    Returns the configuration.
    """
    if 'conf' not in st.session_state:
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        st.session_state.conf=conf
    else:
        conf=st.session_state.conf
    return conf

def generate_button_style_script(widget_class, font_color, background_color='transparent', button_height='50px', font_size='14px'):
    """
    Function to generate a script for styling buttons.
    Parameters like color, background color, height, and font size can be customized.
    Returns the HTML string with the script.
    """
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('.{widget_class}');
            for (var i = 0; i < elements.length; ++i) {{ 
                elements[i].style.color ='{font_color}';
                elements[i].style.background = '{background_color}';
                elements[i].style.height = '{button_height}';
                elements[i].style.fontSize = '{font_size}';
                elements[i].style.width = '100%';
            }}
        </script>
        """
    return htmlstr

def create_navigation_buttons(container):
    """
    Function to create navigation buttons based on the configuration settings.
    The buttons are arranged in a grid layout.
    """
    num_columns = int(load_configuration()['General']['columns'])
    button_height = load_configuration()['General'].get('button_height', '50px')
    num_buttons = len(load_configuration().sections()) - 1
    num_rows = math.ceil(num_buttons / num_columns)
    buttons = []
    scripts = []
    for i in range(num_buttons):
        button_info = load_configuration()[f'Button{i+1}']
        button_class = f'button-{i}'
        code=load_configuration()[f'Button{i+1}']['code']
        origin=st.session_state.location_json['origin']
        url=f'{origin}?code={code}'
        button_html = f'<a href="{url}" target = "_self"><button class="{button_class}">{button_info["label"]}</button></a>'
        buttons.append(button_html)
        scripts.append(generate_button_style_script(button_class, button_info['color'], button_info['background'], button_height, button_info['font_size']))

    for i in range(num_rows):
        row = container.columns(num_columns)
        for j in range(num_columns):
            index = i*num_columns + j
            if index < len(buttons):
                row[j].markdown(buttons[index], unsafe_allow_html=True)
                components.html(scripts[index], height=0, width=0)            

def display_records(col, clear_text):
    """
    Function to display records stored in the session state.
    If 'clear_text' is '1', the input text is cleared after each entry.
    """
    if 'records' in st.session_state:
        st.session_state.records.append(st.session_state['text'])
        for record in st.session_state.records:
            col.write({'code':st.session_state.selected_code,'value':record})
    if clear_text=='1':
        st.session_state['text'] = ''

def get_label_by_code(code):
    """
    Function to get the label associated with a specific code from the configuration settings.
    Returns the label if found, else None.
    """
    for section in load_configuration().sections():
        if 'code' in load_configuration()[section] and load_configuration()[section]['code'] == code:
            return load_configuration()[section]['label']
    return None

def create_barcode_input_area():
    """
    Function to create an input area for barcode entry.
    The input area is associated with a label determined by the selected code.
    """
    label=get_label_by_code(st.session_state.selected_code)
    st.subheader(f':red[{label}]')
    if 'records' not in st.session_state:
        st.session_state.records=[]
    col1, col2 = st.columns(2)
    label=load_configuration()['General']['input_label']
    col1.subheader(f'🔍🔢{label}')
    col1.text_input('', key='text', on_change=display_records, args=[col2,'1'])
    label=load_configuration()['General']['go_back_btn_caption']
    if col1.button(f'🔙{label}', type='primary', use_container_width=True):
        del st.session_state.records
        display_records(col2, '0')
        switch_page('app')
    label=load_configuration()['General']['list_label']
    col2.subheader(f"{label}")
  
# Set the page configuration, load the logo and display the page title
st.set_page_config(layout="wide", menu_items={})

logo=load_configuration()['General']['logo']
if os.path.exists(logo):
    st.image(logo)

st.title(load_configuration()['General']['title'])

# Store the current page location in the session state
if 'location_json' not in st.session_state:
    st.session_state.location_json = get_page_location()

# Set the selected code based on the URL parameters
st.session_state.selected_code=""

if 'code' in st.experimental_get_query_params():
    st.session_state.selected_code=st.experimental_get_query_params()['code'][0]

# If a code is selected, create a barcode input area, else create navigation buttons
if st.session_state.selected_code!="":
    create_barcode_input_area()
else:
    container=st.container()
    create_navigation_buttons(container)
