import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Load Firebase credentials from Streamlit secrets
if not firebase_admin._apps:
    firebase_creds = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

st.set_page_config(page_title="Firebase + Streamlit Demo", page_icon="🔥")
st.markdown("""
<h1 style='text-align: center; color: #ff4b4b;'>Firebase + Streamlit Demo</h1>
<hr style='border:1px solid #ff4b4b;'>
""", unsafe_allow_html=True)

with st.container():
    st.subheader("Add User Data to Firestore")
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input("Name", value="Chirayu")
        role = st.selectbox("Role", ["Student", "Teacher", "Admin"], index=0)
        active = st.checkbox("Active", value=True)
    with col2:
        st.image("images/Sticker_Banana_walnut_cake.png", width=120)

    if st.button("Add Data"):
        doc_ref = db.collection("users").document("test_user")
        doc_ref.set({
            "name": name,
            "role": role,
            "active": active
        })
        st.success(f"User '{name}' added to Firestore!")

st.markdown("---")
st.subheader("All Users in Firestore")
users_ref = db.collection("users")
docs = users_ref.stream()
user_list = []
for doc in docs:
    data = doc.to_dict()
    data["id"] = doc.id
    user_list.append(data)

if user_list:
    st.dataframe(user_list, use_container_width=True)
else:
    st.info("No users found in Firestore.")
