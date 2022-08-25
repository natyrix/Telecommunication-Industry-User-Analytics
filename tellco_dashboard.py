from dashboard import UserOverview, UserEngagement, UserExperience, UserSatisfaction
from multiapp import MultiApp
import streamlit as st
import sys
sys.path.insert(0, './scripts')


# st.set_page_config(page_title="TellCo Telecom Analytics", layout="wide")

app = MultiApp()


st.sidebar.markdown("""
# TellCo's User Analytics
### Multi-Page App
This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).
""")

app.add_app("User Overview Analysis", UserOverview.app)
app.add_app("User Engagement Analysis", UserEngagement.app)
app.add_app("User Experience Analysis", UserExperience.app)
app.add_app("User Satisfaction Analysis", UserSatisfaction.app)

app.run()