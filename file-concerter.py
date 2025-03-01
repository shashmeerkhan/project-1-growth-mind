import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter by Shahmeer", page_icon="📂", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel file to convert it to another format, or clean it.")

files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        if ext == "csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove duplicates - {file.name}"):
            df.drop_duplicates(inplace=True)
            st.success("Duplicates removed")
            st.dataframe(df.head())

        if st.checkbox(f"Remove missing values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("Missing values filled with mean")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select columns to keep - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"Show chart - {file.name}") and not df.select_dtypes(include="number").empty:
            chart_data = df.select_dtypes(include="number").iloc[:, :2]
            st.line_chart(chart_data, use_container_width=True)
            st.success("Chart showing first two numeric columns")

        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)
        
        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")
            
            output.seek(0)
            st.download_button(label=f"Click to download {new_name}", data=output, mime=mime)
            st.success(f"File downloaded successfully: {new_name}")
