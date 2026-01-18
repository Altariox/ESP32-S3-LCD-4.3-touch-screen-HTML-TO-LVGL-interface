#!/usr/bin/env python3
"""
HTML to LVGL Converter for ESP32 Display
Converts HTML/CSS/JS to LVGL C code at build time
"""

import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# Chemins
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "src" / "generated"

class CSSParser:
    def __init__(self, css_content):
        self.styles = {}
        self.parse(css_content)
    
    def parse(self, content):
        # Supprimer les commentaires
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Parser les règles CSS
        rules = re.findall(r'([^{]+)\{([^}]+)\}', content)
        for selector, properties in rules:
            selector = selector.strip()
            props = {}
            for prop in properties.split(';'):
                if ':' in prop:
                    key, value = prop.split(':', 1)
                    props[key.strip()] = value.strip()
            self.styles[selector] = props
    
    def get_style(self, element_id, element_class, element_tag):
        """Récupère le style combiné pour un élément"""
        combined = {}
        
        # Style par tag
        if element_tag in self.styles:
            combined.update(self.styles[element_tag])
        
        # Style par classe
        if element_class:
            for cls in element_class.split():
                class_selector = f".{cls}"
                if class_selector in self.styles:
                    combined.update(self.styles[class_selector])
        
        # Style par ID (priorité max)
        if element_id:
            id_selector = f"#{element_id}"
            if id_selector in self.styles:
                combined.update(self.styles[id_selector])
        
        return combined


class JSParser:
    def __init__(self, js_content):
        self.functions = {}
        self.variables = {}
        self.parse(js_content)
    
    def parse(self, content):
        # Extraire les fonctions avec une meilleure gestion des accolades
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            match = re.match(r'function\s+(\w+)\s*\([^)]*\)\s*\{?', line)
            if match:
                name = match.group(1)
                # Find the function body by counting braces
                brace_count = line.count('{') - line.count('}')
                body_lines = []
                i += 1
                while i < len(lines) and brace_count > 0:
                    body_lines.append(lines[i])
                    brace_count += lines[i].count('{') - lines[i].count('}')
                    i += 1
                body = '\n'.join(body_lines[:-1] if body_lines else [])  # Exclude closing brace
                self.functions[name] = self.convert_to_c(body, name)
            else:
                i += 1
        
        # Extraire les variables globales
        var_pattern = r'var\s+(\w+)\s*=\s*([^;]+);'
        for match in re.finditer(var_pattern, content):
            self.variables[match.group(1)] = match.group(2).strip()
    
    def convert_to_c(self, js_body, func_name):
        """Convertit le corps JS en C approximatif"""
        c_code = []
        brace_depth = 0
        
        for line in js_body.split('\n'):
            line = line.strip()
            if not line or line.startswith('//'):
                if line.startswith('//'):
                    c_code.append(f"    {line}")
                continue
            
            # Track braces for proper else handling
            brace_depth += line.count('{') - line.count('}')
            
            # Clear textarea: setText on input should use lv_textarea_set_text
            if 'setText' in line and 'text-input' in line and '""' in line:
                c_code.append('    lv_textarea_set_text(ui_text_input, "");')
                continue
            
            # setText("id", "value") -> lv_label_set_text(ui_id, "value")
            match = re.match(r'setText\s*\(\s*"([^"]+)"\s*,\s*(.+)\s*\);?$', line)
            if match:
                elem_id = match.group(1).replace('-', '_')
                value = match.group(2).rstrip(';')
                # Gérer la concaténation de strings
                if '+' in value:
                    parts = [p.strip() for p in value.split('+')]
                    c_code.append(f'    static char buf_{func_name}[128];')
                    format_str = ""
                    args = []
                    for p in parts:
                        if p.startswith('"') and p.endswith('"'):
                            format_str += p[1:-1]
                        elif p == 'counter' or p.isdigit():
                            format_str += "%d"
                            args.append(p)
                        else:
                            # String variable
                            format_str += "%s"
                            args.append(p)
                    args_str = ", " + ", ".join(args) if args else ""
                    c_code.append(f'    snprintf(buf_{func_name}, sizeof(buf_{func_name}), "{format_str}"{args_str});')
                    c_code.append(f'    lv_label_set_text(ui_{elem_id}, buf_{func_name});')
                else:
                    c_code.append(f'    lv_label_set_text(ui_{elem_id}, {value});')
                continue
            
            # getText("id") -> lv_textarea_get_text(ui_id)
            match = re.search(r'var\s+(\w+)\s*=\s*getText\s*\(\s*"([^"]+)"\s*\);?', line)
            if match:
                var_name = match.group(1)
                elem_id = match.group(2).replace('-', '_')
                c_code.append(f'    const char* {var_name} = lv_textarea_get_text(ui_{elem_id});')
                continue
            
            # serialSend("command") -> serial_send("command") (extern function in C++)
            match = re.match(r'serialSend\s*\(\s*"([^"]+)"\s*\);?$', line)
            if match:
                command = match.group(1)
                c_code.append(f'    serial_send("{command}");')
                continue
            
            # counter++ ou counter--
            match = re.match(r'(\w+)\+\+;?$', line)
            if match:
                c_code.append(f'    {match.group(1)}++;')
                continue
            match = re.match(r'(\w+)--;?$', line)
            if match:
                c_code.append(f'    {match.group(1)}--;')
                continue
            
            # if (condition) { ... }
            match = re.match(r'if\s*\(\s*(.+)\s*\)\s*\{', line)
            if match:
                cond = match.group(1)
                # text.length > 0 -> strlen(text) > 0
                cond = re.sub(r'(\w+)\.length', r'strlen(\1)', cond)
                c_code.append(f'    if ({cond}) {{')
                continue
            
            if line == '}' or line == '};':
                c_code.append('    }')
                continue
            
            if line == '} else {':
                c_code.append('    } else {')
                continue
        
        return '\n'.join(c_code)


class HTMLToLVGL(HTMLParser):
    def __init__(self, css_parser, js_parser):
        super().__init__()
        self.css = css_parser
        self.js = js_parser
        self.elements = []
        self.current_parent = None
        self.parent_stack = []
        self.element_id = 0
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        elem_id = attrs_dict.get('id', f'elem_{self.element_id}')
        elem_class = attrs_dict.get('class', '')
        onclick = attrs_dict.get('onclick', '')
        placeholder = attrs_dict.get('placeholder', '')
        input_type = attrs_dict.get('type', 'text')
        
        style = self.css.get_style(elem_id, elem_class, tag)
        
        element = {
            'tag': tag,
            'id': elem_id,
            'class': elem_class,
            'style': style,
            'onclick': onclick.replace('()', '') if onclick else '',
            'placeholder': placeholder,
            'type': input_type,
            'text': '',
            'parent': self.current_parent,
            'children': []
        }
        
        if self.current_parent:
            for e in self.elements:
                if e['id'] == self.current_parent:
                    e['children'].append(elem_id)
                    break
        
        self.elements.append(element)
        self.parent_stack.append(self.current_parent)
        self.current_parent = elem_id
        self.element_id += 1
    
    def handle_endtag(self, tag):
        if self.parent_stack:
            self.current_parent = self.parent_stack.pop()
    
    def handle_data(self, data):
        data = data.strip()
        if data and self.elements:
            self.elements[-1]['text'] = data
    
    def generate_c_code(self):
        """Génère le code C pour LVGL"""
        code = []
        code.append('// Auto-generated from HTML/CSS/JS')
        code.append('// Do not edit manually!')
        code.append('')
        code.append('#include "ui_generated.h"')
        code.append('#include <stdio.h>')
        code.append('#include <string.h>')
        code.append('')
        
        # Déclarations des éléments
        code.append('// UI Elements')
        for elem in self.elements:
            if elem['tag'] in ['screen', 'html', 'head', 'body', 'title', 'link', 'script', 'style']:
                continue
            var_name = f"ui_{elem['id'].replace('-', '_')}"
            code.append(f'static lv_obj_t* {var_name};')
        code.append('')
        
        # Variables JS (only simple numeric/string literals)
        if self.js.variables:
            code.append('// Variables')
            for var, val in self.js.variables.items():
                # Only include simple values, not function calls
                if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                    code.append(f'static int {var} = {val};')
                elif val.startswith('"') and val.endswith('"'):
                    code.append(f'static const char* {var} = {val};')
                # Skip complex expressions like function calls
            code.append('')
        
        # Prototypes des fonctions
        code.append('// Function prototypes')
        for func_name in self.js.functions:
            code.append(f'static void {func_name}(void);')
        code.append('')
        
        # Event handlers
        code.append('// Event handlers')
        for elem in self.elements:
            if elem['onclick']:
                handler_name = f"event_{elem['id'].replace('-', '_')}"
                code.append(f'static void {handler_name}(lv_event_t* e) {{')
                code.append(f'    {elem["onclick"]}();')
                code.append('}')
        code.append('')
        
        # Fonctions JS converties
        code.append('// Converted JS functions')
        for func_name, func_body in self.js.functions.items():
            code.append(f'static void {func_name}(void) {{')
            code.append(func_body)
            code.append('}')
            code.append('')
        
        # Fonction de création UI
        code.append('void ui_generated_init(lv_obj_t* parent) {')
        code.append('    // Set screen background')
        
        screen_style = self.css.get_style(None, None, 'screen')
        if 'bg-color' in screen_style:
            color = self.parse_color(screen_style['bg-color'])
            code.append(f'    lv_obj_set_style_bg_color(parent, lv_color_hex({color}), 0);')
        
        code.append('')
        
        # Créer les éléments
        for elem in self.elements:
            if elem['tag'] in ['screen', 'html', 'head', 'body', 'title', 'link', 'script', 'style']:
                continue
            
            var_name = f"ui_{elem['id'].replace('-', '_')}"
            parent_var = 'parent'
            if elem['parent'] and elem['parent'] not in ['main', 'body']:
                parent_var = f"ui_{elem['parent'].replace('-', '_')}"
            
            code.append(f'    // {elem["tag"]}#{elem["id"]}')
            
            if elem['tag'] == 'label':
                code.append(f'    {var_name} = lv_label_create({parent_var});')
                if elem['text']:
                    code.append(f'    lv_label_set_text({var_name}, "{elem["text"]}");')
            
            elif elem['tag'] == 'button':
                code.append(f'    {var_name} = lv_btn_create({parent_var});')
                btn_label_var = None
                if elem['text']:
                    btn_label_var = f"{var_name}_label"
                    code.append(f'    lv_obj_t* {btn_label_var} = lv_label_create({var_name});')
                    code.append(f'    lv_label_set_text({btn_label_var}, "{elem["text"]}");')
                    code.append(f'    lv_obj_center({btn_label_var});')
                if elem['onclick']:
                    handler = f"event_{elem['id'].replace('-', '_')}"
                    code.append(f'    lv_obj_add_event_cb({var_name}, {handler}, LV_EVENT_CLICKED, NULL);')
            
            elif elem['tag'] == 'input':
                code.append(f'    {var_name} = lv_textarea_create({parent_var});')
                code.append(f'    lv_textarea_set_one_line({var_name}, true);')
                if elem['placeholder']:
                    code.append(f'    lv_textarea_set_placeholder_text({var_name}, "{elem["placeholder"]}");')
            
            elif elem['tag'] == 'div':
                code.append(f'    {var_name} = lv_obj_create({parent_var});')
                code.append(f'    lv_obj_clear_flag({var_name}, LV_OBJ_FLAG_SCROLLABLE);')
            
            # Appliquer les styles
            style = elem['style']
            if elem['tag'] == 'button':
                self.apply_style(code, var_name, style, parent_var, text_target_var=btn_label_var)
            else:
                self.apply_style(code, var_name, style, parent_var)
            
            code.append('')
        
        # Appeler init() si elle existe
        if 'init' in self.js.functions:
            code.append('    // Call init function')
            code.append('    init();')
        
        code.append('}')
        
        return '\n'.join(code)
    
    def apply_style(self, code, var_name, style, parent_var, text_target_var=None):
        """Applique les styles CSS à un élément LVGL"""
        if 'width' in style:
            code.append(f'    lv_obj_set_width({var_name}, {style["width"]});')
        if 'height' in style:
            code.append(f'    lv_obj_set_height({var_name}, {style["height"]});')
        
        # Position
        x = style.get('x', 'center')
        y = style.get('y', '0')
        
        if x == 'center' and y != 'center':
            code.append(f'    lv_obj_align({var_name}, LV_ALIGN_TOP_MID, 0, {y});')
        elif x != 'center' and y == 'center':
            code.append(f'    lv_obj_align({var_name}, LV_ALIGN_LEFT_MID, {x}, 0);')
        elif x == 'center' and y == 'center':
            code.append(f'    lv_obj_center({var_name});')
        else:
            code.append(f'    lv_obj_set_pos({var_name}, {x}, {y});')
        
        if 'bg-color' in style:
            color = self.parse_color(style['bg-color'])
            code.append(f'    lv_obj_set_style_bg_color({var_name}, lv_color_hex({color}), 0);')
            code.append(f'    lv_obj_set_style_bg_opa({var_name}, LV_OPA_COVER, 0);')
        
        if 'text-color' in style:
            color = self.parse_color(style['text-color'])
            code.append(f'    lv_obj_set_style_text_color({var_name}, lv_color_hex({color}), 0);')
            if text_target_var:
                code.append(f'    lv_obj_set_style_text_color({text_target_var}, lv_color_hex({color}), 0);')
        
        if 'border-radius' in style:
            code.append(f'    lv_obj_set_style_radius({var_name}, {style["border-radius"]}, 0);')
        
        if 'padding' in style:
            code.append(f'    lv_obj_set_style_pad_all({var_name}, {style["padding"]}, 0);')
        
        if 'font-size' in style:
            size = int(style['font-size'])
            # Map CSS font-size to an enabled LVGL font.
            # Keep this conservative to avoid requiring many fonts.
            if size >= 44:
                font = 'lv_font_montserrat_48'
            elif size >= 24:
                font = 'lv_font_montserrat_30'
            else:
                font = 'lv_font_montserrat_14'

            code.append(f'    lv_obj_set_style_text_font({var_name}, &{font}, 0);')
            if text_target_var:
                code.append(f'    lv_obj_set_style_text_font({text_target_var}, &{font}, 0);')
    
    def parse_color(self, color_str):
        """Convertit une couleur CSS en hex LVGL"""
        color_str = color_str.strip()
        if color_str.startswith('#'):
            return '0x' + color_str[1:].upper()
        return '0xFFFFFF'


def main():
    print("=" * 50)
    print("HTML to LVGL Converter")
    print("=" * 50)
    
    # Créer le dossier de sortie
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Lire les fichiers
    html_file = DATA_DIR / "index.html"
    css_file = DATA_DIR / "style.css"
    js_file = DATA_DIR / "script.js"
    
    if not html_file.exists():
        print(f"Error: {html_file} not found!")
        sys.exit(1)
    
    html_content = html_file.read_text()
    css_content = css_file.read_text() if css_file.exists() else ""
    js_content = js_file.read_text() if js_file.exists() else ""
    
    print(f"Reading: {html_file}")
    print(f"Reading: {css_file}")
    print(f"Reading: {js_file}")
    
    # Parser
    css_parser = CSSParser(css_content)
    js_parser = JSParser(js_content)
    html_parser = HTMLToLVGL(css_parser, js_parser)
    html_parser.feed(html_content)
    
    # Générer le code C
    c_code = html_parser.generate_c_code()
    
    # Header file
    header = '''// Auto-generated from HTML/CSS/JS
// Do not edit manually!

#ifndef UI_GENERATED_H
#define UI_GENERATED_H

#include "lvgl.h"

#ifdef __cplusplus
extern "C" {
#endif

// Extern function implemented in main.cpp for serial communication
extern void serial_send(const char* message);

void ui_generated_init(lv_obj_t* parent);

#ifdef __cplusplus
}
#endif

#endif // UI_GENERATED_H
'''
    
    # Écrire les fichiers
    c_output = OUTPUT_DIR / "ui_generated.c"
    h_output = OUTPUT_DIR / "ui_generated.h"
    
    c_output.write_text(c_code)
    h_output.write_text(header)
    
    print(f"Generated: {c_output}")
    print(f"Generated: {h_output}")
    print("=" * 50)
    print("Conversion complete!")


if __name__ == "__main__":
    main()
