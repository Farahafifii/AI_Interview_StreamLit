import streamlit as st
from streamlit.components.v1 import html

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)
def main():
    st.title('Interview Warmup')
    st.markdown('Prepare yourself for success.')

    job_title = st.radio("What is your Job Title", ("Data Analyst", "Cyber Security Analyst", "Networks Engineer"))
    question_types = st.multiselect("Type of Questions",
                                    ["Technical Questions", "Behavioural Questions", "Scenario Questions"])
    difficulty = st.radio("Level of Difficulty for Questions", ("Beginner", "Intermediate", "Challenging"))
    notes = st.text_area("Other Notes", max_chars=100)

    # Add some spacing and organize widgets into columns
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("")  # Empty space for layout adjustment

    with col2:
        if st.button("Submit and Start"):
            st.session_state['jobTitle'] = job_title
            st.session_state['questionType'] = question_types
            st.session_state['difficulty'] = difficulty
            st.session_state['notes'] = notes
            nav_page("main")


if __name__ == '__main__':
    main()
