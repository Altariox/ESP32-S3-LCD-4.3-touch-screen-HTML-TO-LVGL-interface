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
    # Tags that are self-closing or void elements
    VOID_TAGS = {'img', 'input', 'br', 'hr', 'meta', 'link', 'area', 'base', 'col', 'embed', 'param', 'source', 'track', 'wbr'}
    
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
        src = attrs_dict.get('src', '')
        data_icon = attrs_dict.get('data-icon', '')
        
        style = self.css.get_style(elem_id, elem_class, tag)
        
        element = {
            'tag': tag,
            'id': elem_id,
            'class': elem_class,
            'style': style,
            'onclick': onclick.replace('()', '') if onclick else '',
            'placeholder': placeholder,
            'type': input_type,
            'src': src,
            'data_icon': data_icon,
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
        self.element_id += 1
        
        # For void/self-closing tags, don't push to parent stack
        # They can't have children, so don't change current_parent
        if tag.lower() not in self.VOID_TAGS:
            self.parent_stack.append(self.current_parent)
            self.current_parent = elem_id
    
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
        code.append('#include "ui_assets.h"')
        code.append('#include <stdio.h>')
        code.append('#include <string.h>')
        code.append('')
        
        # Déclarations des éléments
        # Some labels need to be externally accessible for dynamic updates
        dynamic_labels = ['time_display', 'date_display', 'temp_value', 'weather_desc', 'humidity', 'wind']
        
        code.append('// UI Elements')
        for elem in self.elements:
            if elem['tag'] in ['screen', 'html', 'head', 'body', 'title', 'link', 'script', 'style']:
                continue
            var_name = f"ui_{elem['id'].replace('-', '_')}"
            elem_id_clean = elem['id'].replace('-', '_')
            # Make dynamic labels non-static (externally accessible)
            if elem_id_clean in dynamic_labels:
                code.append(f'lv_obj_t* {var_name} = NULL;')
            else:
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
        
        # Detect multiple screens for tileview
        screens = [e for e in self.elements if e['tag'] == 'screen']
        use_tileview = len(screens) > 1
        
        # Fonction de création UI
        code.append('void ui_generated_init(lv_obj_t* parent) {')
        
        if use_tileview:
            # Create tileview for multiple screens (swipeable pages)
            code.append('    // Create tileview for swipeable pages')
            code.append('    static lv_obj_t* tileview;')
            code.append('    tileview = lv_tileview_create(parent);')
            code.append('    lv_obj_set_size(tileview, 800, 480);')
            code.append('    lv_obj_set_style_bg_opa(tileview, LV_OPA_TRANSP, 0);')
            code.append('')
            
            # Create tiles for each screen
            for idx, screen in enumerate(screens):
                screen_id = screen['id'].replace('-', '_')
                screen_style = self.css.get_style(screen['id'], None, 'screen')
                bg_color = self.parse_color(screen_style.get('bg-color', '#1a1a2e'))
                
                code.append(f'    // Tile {idx}: {screen["id"]}')
                code.append(f'    static lv_obj_t* tile_{screen_id};')
                code.append(f'    tile_{screen_id} = lv_tileview_add_tile(tileview, {idx}, 0, LV_DIR_HOR);')
                code.append(f'    lv_obj_set_style_bg_color(tile_{screen_id}, lv_color_hex({bg_color}), 0);')
                code.append(f'    lv_obj_set_style_bg_opa(tile_{screen_id}, LV_OPA_COVER, 0);')
                code.append('')
        else:
            code.append('    // Set screen background')
            screen_style = self.css.get_style(None, None, 'screen')
            if 'bg-color' in screen_style:
                color = self.parse_color(screen_style['bg-color'])
                code.append(f'    lv_obj_set_style_bg_color(parent, lv_color_hex({color}), 0);')
            code.append('')
        
        # Build screen ID list for parent resolution
        screen_ids = [s['id'] for s in screens] if use_tileview else []
        
        # Créer les éléments
        for elem in self.elements:
            if elem['tag'] in ['screen', 'html', 'head', 'body', 'title', 'link', 'script', 'style']:
                continue
            
            var_name = f"ui_{elem['id'].replace('-', '_')}"
            parent_var = 'parent'
            
            # Determine parent
            if elem['parent']:
                if use_tileview and elem['parent'] in screen_ids:
                    # Parent is a screen -> use the tile
                    parent_var = f"tile_{elem['parent'].replace('-', '_')}"
                elif elem['parent'] not in ['main', 'body']:
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

            elif elem['tag'] == 'img':
                code.append(f'    {var_name} = lv_img_create({parent_var});')
                if elem.get('data_icon'):
                    icon_sym = re.sub(r'[^a-zA-Z0-9_]', '_', elem['data_icon']).lower()
                    code.append(f'    lv_img_set_src({var_name}, &ui_img_{icon_sym});')
                else:
                    code.append(f'    // WARNING: img#{elem["id"]} is missing data-icon; no source set')
            
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
            # Fonts enabled: 14, 30, 36, 40, 44, 48
            if size >= 100:
                font = 'lv_font_montserrat_48'  # Largest available
            elif size >= 60:
                font = 'lv_font_montserrat_48'
            elif size >= 44:
                font = 'lv_font_montserrat_44'
            elif size >= 40:
                font = 'lv_font_montserrat_40'
            elif size >= 36:
                font = 'lv_font_montserrat_36'
            elif size >= 24:
                font = 'lv_font_montserrat_30'
            else:
                font = 'lv_font_montserrat_14'

            code.append(f'    lv_obj_set_style_text_font({var_name}, &{font}, 0);')
            if text_target_var:
                code.append(f'    lv_obj_set_style_text_font({text_target_var}, &{font}, 0);')
        
        # Transform zoom support - scale(X) in CSS
        if 'transform' in style:
            transform = style['transform']
            scale_match = re.search(r'scale\s*\(\s*([\d.]+)\s*\)', transform)
            if scale_match:
                scale = float(scale_match.group(1))
                # LVGL zoom: 256 = 100%, so scale * 256
                zoom_val = int(scale * 256)
                code.append(f'    lv_obj_set_style_transform_zoom({var_name}, {zoom_val}, 0);')
                # Need to set transform pivot to center for proper scaling
                code.append(f'    lv_obj_set_style_transform_pivot_x({var_name}, LV_PCT(50), 0);')
                code.append(f'    lv_obj_set_style_transform_pivot_y({var_name}, LV_PCT(50), 0);')
    
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
    
    # Header file with extern declarations for dynamic labels
    # Identify labels that should be externally accessible
    dynamic_labels = ['time_display', 'date_display', 'temp_value', 'weather_desc', 'humidity', 'wind']
    
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

// Dynamic labels accessible from main.cpp for updates
'''
    for label_id in dynamic_labels:
        header += f'extern lv_obj_t* ui_{label_id};\n'
    
    header += '''
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
