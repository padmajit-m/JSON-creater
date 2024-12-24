import pandas as pd
import json
from fuzzywuzzy import process
import streamlit as st

# Load mapping template
def load_template(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

# Generate JSON mapping
def generate_json(headers, mapping_template, selected_columns):
    result = {"excelMappings": {}}
    for header, selected_column in zip(headers, selected_columns):
        if selected_column in mapping_template:
            result["excelMappings"][header] = mapping_template[selected_column]
        else:
            result["excelMappings"][header] = {"dbTableName": "Unmapped", "dbColumnName": header}
    return result

# Streamlit UI
st.title("Dynamic JSON Mapping Tool")
st.write("Upload the partner file and template JSON to generate mappings.")

# File uploads
partner_file = st.file_uploader("Upload Partner File (Excel/CSV)", type=["xlsx", "csv"])
template_file = st.file_uploader("Upload Mapping JSON Template", type="json")

if partner_file and template_file:
    # Read files
    file_ext = partner_file.name.split('.')[-1]
    data = pd.read_excel(partner_file) if file_ext == 'xlsx' else pd.read_csv(partner_file)
    headers = data.columns.tolist()
    mapping_template = load_template(template_file)

    # UI for header mapping
    st.write("Map Partner File Headers:")
    selected_columns = []
    for header in headers:
        st.text_input(f"Header Name: {header}", value=header, key=f"text_{header}")
        options = list(mapping_template["excelMappings"].keys())
        selected = st.selectbox(f"Map '{header}' to:", options, key=f"dropdown_{header}")
        selected_columns.append(selected)

    # Generate and display JSON
    if st.button("Generate JSON"):
        output_json = generate_json(headers, mapping_template["excelMappings"], selected_columns)
        st.json(output_json)

        # Option to download JSON
        json_str = json.dumps(output_json, indent=4)
        st.download_button("Download JSON", json_str, file_name="partner_mapping.json", mime="application/json")
