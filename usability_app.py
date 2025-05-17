import streamlit as st
import pandas as pd
import time
import os

# Create data folder if it doesn't exist
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define file paths
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")

# Save data function
def save_to_csv(data_dict, csv_file):
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        df_new.to_csv(csv_file, mode='a', header=False, index=False)

# Load data function
def load_from_csv(csv_file):
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()

def main():
    st.title("Automated Usability Testing Tool")

    home, consent, demographics, tasks, exit, report = st.tabs([
        "Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"])

    with home:
        st.header("Welcome")
        st.write("""
            This app will guide you through a usability test.

            Steps:
            1. Consent
            2. Demographics
            3. Complete Tasks
            4. Exit Feedback
            5. View Summary Report
        """)

    with consent:
        st.header("Consent Form")
        st.write("""
            By participating, you agree that your responses will be collected
            for usability research purposes only.
        """)
        consent_given = st.checkbox("I agree to participate in this usability test.")
        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("You must agree to the consent terms before proceeding.")
            else:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                }
                save_to_csv(data_dict, CONSENT_CSV)
                st.success("Consent recorded.")

    with demographics:
        st.header("Demographic Questionnaire")
        with st.form("demographic_form"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=10, max_value=100, step=1)
            occupation = st.text_input("Occupation")
            familiarity = st.radio("Familiarity with similar tools:", ["None", "Some", "Experienced"])
            submitted = st.form_submit_button("Submit Demographics")
            if submitted:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "age": age,
                    "occupation": occupation,
                    "familiarity": familiarity
                }
                save_to_csv(data_dict, DEMOGRAPHIC_CSV)
                st.success("Demographic data saved.")

    with tasks:
        st.header("Task Page")
        selected_task = st.selectbox("Select Task", ["Task 1: Example Task"])
        st.write("Task: Locate and click on the profile icon.")

        if st.button("Start Task Timer"):
            st.session_state["start_time"] = time.time()
        if st.button("Stop Task Timer") and "start_time" in st.session_state:
            duration = time.time() - st.session_state["start_time"]
            st.session_state["task_duration"] = duration

        success = st.radio("Task completion status:", ["Yes", "No", "Partial"])
        notes = st.text_area("Observer Notes")

        if st.button("Save Task Results"):
            duration_val = st.session_state.get("task_duration", "")
            data_dict = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "task_name": selected_task,
                "success": success,
                "duration_seconds": duration_val,
                "notes": notes
            }
            save_to_csv(data_dict, TASK_CSV)
            st.success("Task data saved.")
            st.session_state.pop("start_time", None)
            st.session_state.pop("task_duration", None)

    with exit:
        st.header("Exit Questionnaire")
        with st.form("exit_form"):
            satisfaction = st.slider("Rate your satisfaction (1=Low, 5=High):", 1, 5, 3)
            difficulty = st.slider("Rate task difficulty (1=Easy, 5=Hard):", 1, 5, 3)
            open_feedback = st.text_area("Additional Comments")
            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "satisfaction": satisfaction,
                    "difficulty": difficulty,
                    "open_feedback": open_feedback
                }
                save_to_csv(data_dict, EXIT_CSV)
                st.success("Exit questionnaire data saved.")

    with report:
        st.header("Usability Report")

        st.subheader("Consent Data")
        consent_df = load_from_csv(CONSENT_CSV)
        st.dataframe(consent_df if not consent_df.empty else pd.DataFrame([{"Status":"No data"}]))

        st.subheader("Demographic Data")
        demo_df = load_from_csv(DEMOGRAPHIC_CSV)
        st.dataframe(demo_df if not demo_df.empty else pd.DataFrame([{"Status":"No data"}]))

        st.subheader("Task Performance Data")
        task_df = load_from_csv(TASK_CSV)
        st.dataframe(task_df if not task_df.empty else pd.DataFrame([{"Status":"No data"}]))

        st.subheader("Exit Questionnaire Data")
        exit_df = load_from_csv(EXIT_CSV)
        st.dataframe(exit_df if not exit_df.empty else pd.DataFrame([{"Status":"No data"}]))

        if not exit_df.empty:
            st.subheader("Aggregated Feedback")
            st.write(f"**Average Satisfaction**: {exit_df['satisfaction'].mean():.2f}")
            st.write(f"**Average Difficulty**: {exit_df['difficulty'].mean():.2f}")

if __name__ == "__main__":
    main()
