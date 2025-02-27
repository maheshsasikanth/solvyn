import streamlit as st
from PIL import Image
import numpy as np
import datetime
import google.generativeai as genai
import io
import os

def main():
    if st.session_state.get("logged_in"):
        show_landing_page()
    elif st.session_state.get("create_account"):
        show_create_account_page()
    else:
        show_login_page()

def show_login_page():
    st.markdown(
        """
        <style>
        body {
            background-color: white;
        }
        h1 {
            color: #0000FF;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    #image = Image.fromarray(np.random.randint(0, 255, (200, 300, 3), dtype=np.uint8))

    #col1, col2, col3 = st.columns([1, 2, 1]) # adjust the column ratio for your needs.

    #with col2:
       # st.image("/Users/maheshsasikanth/Downloads/solvyns.png", width=300)
    #st.markdown('<div class="center"><img src="solvyn.png" width="300"></div>', unsafe_allow_html=True)
    #st.image("/Users/maheshsasikanth/Downloads/solvyns.png", width=200)
    #st.logo("/Users/maheshsasikanth/Downloads/solvyn.png", size = "large")
    st.title("Health Compass Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if validate_credentials(username, password):
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.markdown("#### Alternatively, you can login with Google")

    if st.button("Login with Google"):
        # Here you would add the logic to handle Google login
        st.session_state.logged_in = True
        st.session_state.username = "Google User"
        st.success("Logged in with Google!")
        st.rerun()

    st.markdown("---")
    st.markdown("### New User ?")

    if st.button("Create Account"):
        st.session_state.create_account = True
        st.rerun()

def show_create_account_page():
    st.markdown(
        """
        <style>
        body {
            background-color: white;
        }
        h1 {
            color: teal;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Create Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=1, max_value=150, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    city = st.text_input("City")
    password = st.text_input("Password", type="password")

    if st.button("Create"):
        if create_account(name, email, age, gender, city, password):
            st.success("Account created successfully! Please login.")
            st.session_state.create_account = False
            st.rerun()
        else:
            st.error("Account creation failed. Please try again.")

    if st.button("Back to Login"):
        st.session_state.create_account = False
        st.rerun()

def show_landing_page():

    #image = Image.fromarray(np.random.randint(0, 255, (200, 300, 3), dtype=np.uint8))

    #col1, col2, col3 = st.sidebar.columns([2, 2, 2]) # adjust the column ratio for your needs.

    #with col2:
        #st.sidebar.image("/Users/maheshsasikanth/Downloads/solvyns.png", use_container_width=True)

    #st.sidebar.image("/Users/maheshsasikanth/Downloads/solvyns.png", width=200)
    st.sidebar.markdown(
        """
        <style>
        .css-1d391kg {
            background-color: #FFFDD0;
        }
        </style>
        <div style="text-align: center;">
            <h1>Navigation</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )



    sections = {
        "Member Profile": "🧑‍⚕️",
        "Reports": "📊",
        "Consultations": "🗣️",
        "Prescriptions": "💊"
    }
    for section, icon in sections.items():
        if st.sidebar.button(f"{icon} {section}", key=section, use_container_width=True):
            st.session_state.section = section

    section = st.session_state.get("section", "Member Profile")

    #image = Image.fromarray(np.random.randint(0, 255, (200, 300, 3), dtype=np.uint8))

    #col1, col2, col3 = st.columns([1, 2, 1]) # adjust the column ratio for your needs.

    #with col2:
        #st.image("/Users/maheshsasikanth/Downloads/solvyns.png", width=200)

    st.markdown(
        """
        <style>
        body {
            background-color: white;
        }
        h1, h2, h3, h4, h5, h6 {
            color: teal;
        }
        hr {
            border-top: 1px dotted lightblue;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    #st.markdown(f'<div style="text-align: right;">Username: {st.session_state.username}</div>', unsafe_allow_html=True)

    #st.markdown("---")

    if section == "Member Profile":
        st.header("Member Summary")

        user_data = get_user_data(st.session_state.username)

        if user_data:
            col1, col2, col3 = st.columns([2, 2, 3])

            with col1:
                st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="color: teal;">Basic Info</h3>
                    <p><strong>Name:</strong> {user_data['name']}</p>
                    <p><strong>Gender:</strong> {user_data['gender']}</p>
                    <p><strong>City:</strong> {user_data['city']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="color: teal;">Health Stats</h3>
                    <p><strong>Age:</strong> 34</p>
                    <p><strong>Height:</strong> 184cm</p>
                    <p><strong>Weight:</strong> 85kg</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="color: teal;">Upcoming</h3>
                    <p><strong>Appointment Date:</strong> 1st March, 2025</p>
                    <p><strong>Appointment with:</strong> Dr. Ramya</p>
                    <p><strong>Test:</strong> CUE</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("User data not found.")

        st.markdown("---")

        st.header("Overall Health Status")
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            st.markdown(
            """
            <style>
            .health-status-tile {
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            .health-status-tile h1 {
                font-size: 48px;
                color: #FF5733;
                margin: 0;
            }
            .health-status-tile p {
                font-size: 18px;
                color: #333;
                margin: 0;
            }
            </style>
            <div class="health-status-tile">
                <h1>~40%</h1>
                <p>Bad</p>
            </div>
            """,
            unsafe_allow_html=True,
            )

        st.markdown("---")
        st.header("Recommended Actions")

        actions = [
            {"Action Item": "Take Lipid Profile Test", "Last Test Date": "6/1/2024", "Due Date": "1/1/2025"},
            {"Action Item": "Take hba1c Test", "Last Test Date": "6/1/2024", "Due Date": "1/1/2025"},
            {"Action Item": "Take Thyroid Test", "Last Test Date": "6/1/2024", "Due Date": "3/1/2025"},
        ]

        current_date = datetime.datetime.now().date()

        def format_row(action, index):
            due_date = datetime.datetime.strptime(action["Due Date"], "%m/%d/%Y").date()
            due_date_color = "red" if due_date < current_date else "black"
            return f'<tr><td style="width: 5%;">{index + 1}</td><td>{action["Action Item"]}</td><td>{action["Last Test Date"]}</td><td style="color: {due_date_color};">{action["Due Date"]}</td></tr>'

        table_html = """
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #ddd;
        }
        </style>
        <table>
            <thead>
            <tr>
            <th style="width: 5%;">#</th>
            <th>Action Item</th>
            <th>Last Test Date</th>
            <th>Due Date</th>
            </tr>
            </thead>
            <tbody>
        """
        for index, action in enumerate(actions):
            table_html += format_row(action, index)
        table_html += "</tbody></table>"

        st.markdown(table_html, unsafe_allow_html=True)


        st.markdown("---")
        st.header("Active Conditions")
        st.markdown(
            """
            <style>
            .condition {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
            }
            .condition h4 {
            color: teal;
            margin: 0;
            }
            .condition p {
            margin: 5px 0 0 0;
            }
            </style>
            <div class="condition">
            <h4>Hypothyroidism</h4>
            <p>Currently on 50mcg 6 days a week</p>
            </div>
            <div class="condition">
            <h4>Vitamin B12 Deficiency</h4>
            <p>Currently on MultiNeuron 1 tab per day</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.header("Health Documents")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Uploaded Documents")
            if "uploaded_files" in st.session_state and st.session_state.uploaded_files:
                for file_name in st.session_state.uploaded_files:
                    st.write(file_name)
            else:
                st.write("No documents uploaded yet.")

        with col2:
            st.subheader("Upload Document")
            document_type = st.selectbox("Select Document Type", ["Reports", "Consultation Notes", "Prescriptions"])
            uploaded_file = st.file_uploader(f"Upload {document_type}", type=["pdf", "png", "jpg", "jpeg"])

            if uploaded_file is not None:
                if "uploaded_files" not in st.session_state:
                    st.session_state.uploaded_files = []
                st.session_state.uploaded_files.append(uploaded_file.name)
                st.write(f"File '{uploaded_file.name}' uploaded successfully.")
                st.rerun()

    elif section == "Reports":
        st.header("Reports")
        

        gemini_api_key = st.text_input("Enter your Gemini API Key", type="password")

        # File Upload
        uploaded_file = st.file_uploader("Upload a document (PDF, TXT)", type=["pdf", "txt"])

        if uploaded_file and gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-lite')

            if uploaded_file.type == "application/pdf":
                try:
                    import pypdf

                    pdf_reader = pypdf.PdfReader(io.BytesIO(uploaded_file.getvalue()))
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() or "" #Handle cases where page.extract_text() returns None.

                except ImportError:
                    st.error("Please install pypdf: pip install pypdf")
                    st.stop()
                except Exception as e:
                    st.error(f"Error processing PDF: {e}")
                    st.stop()

            elif uploaded_file.type == "text/plain":
                text = uploaded_file.getvalue().decode("utf-8")

            else:
                st.error("Unsupported file type. Please upload a PDF or TXT file.")
                st.stop()

            if text:
                prompt = f"Summarize the following document:\n\n{text}\n\nSummary:"
                try:
                    response = model.generate_content(prompt)
                    st.subheader("Summary:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error generating summary: {e}")

        else:
            if not gemini_api_key and uploaded_file:
                st.warning("Please enter your Gemini API key.")
            if gemini_api_key and not uploaded_file:
                st.warning("Please upload a document.")
            if not gemini_api_key and not uploaded_file:
                st.info("Upload a document and enter your Gemini API key to get a summary.")

    elif section == "Consultations":
        st.header("Consultations")
        st.write("Here you can view your consultation history.")

    elif section == "Prescriptions":
        st.header("Prescriptions")
        st.write("Here you can view your prescriptions.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.session_state.uploaded_files = []
        st.session_state.page_loaded = False
        st.rerun()

    # Add floating chatbot icon
    st.components.v1.html(
        """
        <style>
        .chatbot-icon {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #007bff;
            color: white;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            cursor: pointer;
            z-index: 1000;
        }
        </style>
        <div class="chatbot-icon" onclick="document.getElementById('chatbot').style.display='block'">💬</div>
        <div id="chatbot" style="display:none; position:fixed; bottom:80px; right:20px; width:300px; height:400px; background:white; border:1px solid #ccc; border-radius:10px; z-index:1000;">
            <div style="padding:10px; background:#007bff; color:white; border-top-left-radius:10px; border-top-right-radius:10px;">
                <span style="float:left;">Health Bot</span>
                <span style="float:right; cursor:pointer;" onclick="document.getElementById('chatbot').style.display='none'">✖</span>
            </div>
            <div style="padding:10px; height:calc(100% - 60px); overflow-y:auto;">
                <div id="chat-history"></div>
                <input type="text" id="chat-input" style="width:calc(100% - 20px); padding:5px; margin-top:10px;" placeholder="Ask the Health Bot...">
                <button onclick="sendMessage()" style="width:100%; padding:5px; margin-top:5px;">Send</button>
            </div>
        </div>
        <script>
        function sendMessage() {
            var input = document.getElementById('chat-input');
            var message = input.value;
            if (message) {
                var chatHistory = document.getElementById('chat-history');
                var userMessage = document.createElement('div');
                userMessage.textContent = 'User: ' + message;
                chatHistory.appendChild(userMessage);
                input.value = '';
                // Simulate bot response
                setTimeout(function() {
                    var botMessage = document.createElement('div');
                    botMessage.textContent = 'Bot: ' + getBotResponse(message);
                    chatHistory.appendChild(botMessage);
                    chatHistory.scrollTop = chatHistory.scrollHeight;
                }, 1000);
            }
        }
        function getBotResponse(message) {
            if (message.toLowerCase().includes('health')) {
                return 'Maintaining a balanced diet and regular exercise is important for overall health.';
            } else if (message.toLowerCase().includes('exercise')) {
                return 'Try to get at least 30 minutes of moderate exercise most days of the week.';
            } else {
                return 'I\'m still learning. Please ask me about health or exercise.';
            }
        }
        </script>
        """,
        height=500,
    )

def validate_credentials(username, password):
    if username == "user" and password == "password":
        return True
    else:
        return False

def get_user_data(username):
    if username == "user":
        return {"name": "Mahesh Sasikanth", "age": 34, "gender": "Male", "city": "Hyderabad"}
    else:
        return None

def get_bot_response(user_input):
    if "health" in user_input.lower():
        return "Maintaining a balanced diet and regular exercise is important for overall health."
    elif "exercise" in user_input.lower():
        return "Try to get at least 30 minutes of moderate exercise most days of the week."
    else:
        return "I'm still learning. Please ask me about health or exercise."

def create_account(name, email, age, gender, city, password):
    st.session_state.user_data = {
        "name": name,
        "email": email,
        "age": age,
        "gender": gender,
        "city": city,
        "password": password,
    }
    return True

if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "page_loaded" not in st.session_state:
        st.session_state.page_loaded = False
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "create_account" not in st.session_state:
        st.session_state.create_account = False
    if "section" not in st.session_state:
        st.session_state.section = "Member Profile"

    main()