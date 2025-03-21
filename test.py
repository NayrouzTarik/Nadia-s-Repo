import streamlit as st
import pandas as pd

# Load the Excel files
data_prof_fst = pd.read_excel("DATA PROF FST.xlsx", sheet_name=None)
classeur_excel_1 = pd.read_excel("Classeur Excel 1.xlsx", sheet_name=None)

# Function to check for conflicts
def check_conflicts(filiere, module_s1, module_s3, day, time_slot):
    conflicts = []
    if filiere in classeur_excel_1:
        df = classeur_excel_1[filiere]
        # Check if the selected modules are in the timetable for the given day and time slot
        if day in df.columns:
            s1_conflict = df[df[day].str.contains(module_s1, case=False, na=False)]
            s3_conflict = df[df[day].str.contains(module_s3, case=False, na=False)]
            if not s1_conflict.empty and not s3_conflict.empty:
                common_students = s1_conflict.index.tolist()  # Assuming index contains student IDs
                conflicts.extend(common_students)
    return list(set(conflicts))  # Remove duplicates

# Streamlit UI
st.title("Gestion d'Emploi du Temps Sans Chevauchement")

# Dropdown for Filiere selection
filieres = ["GEGM", "BCG", "MIPC", "MIP"]
selected_filiere = st.selectbox("Choisissez la Filiere:", filieres)

# Dropdown for Module selection based on selected Filiere
modules_s1 = set()
modules_s3 = set()

# Possible column names for modules
s1_columns = ["MODULE(S1)", "MODULE(S1)A", "MODULE(S1)B"]
s3_columns = ["MODULES (S3)", "MODULES (S3)A", "MODULES (S3)B"]

if selected_filiere in data_prof_fst:
    df = data_prof_fst[selected_filiere]
    for col in s1_columns:
        if col in df.columns:
            modules_s1.update(df[col].dropna().tolist())
    for col in s3_columns:
        if col in df.columns:
            modules_s3.update(df[col].dropna().tolist())

selected_module_s1 = st.selectbox("Choisissez le Module S1:", list(modules_s1))
selected_module_s3 = st.selectbox("Choisissez le Module S3:", list(modules_s3))

# Dropdown for Day selection
days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
selected_day = st.selectbox("Choisissez le Jour:", days)

# Dropdown for Time Slot selection
time_slots = ["09h00 - 10h45", "11h00 - 12h45", "13h00 - 14h45", "15h00 - 16h45", "17h00 - 18h30"]
selected_time_slot = st.selectbox("Choisissez le Créneau Horaires:", time_slots)

# Button to check for conflicts
if st.button("Vérifier les Conflits"):
    conflicts = check_conflicts(selected_filiere, selected_module_s1, selected_module_s3, selected_day, selected_time_slot)
    if conflicts:
        st.write("Conflits détectés :")
        for student in conflicts:
            st.write(student)
    else:
        st.write("Aucun conflit détecté.")

# Display the timetable for the selected Filiere
if selected_filiere in classeur_excel_1:
    st.write(f"Emploi du Temps pour la Filiere {selected_filiere}:")
    st.dataframe(classeur_excel_1[selected_filiere])
