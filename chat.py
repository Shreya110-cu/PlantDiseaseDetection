import streamlit as st

def main():
    st.title("🌾 AgriVision Chatbot")
    
    # Initialize session state variables if not present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for chat in st.session_state.chat_history:
        role, message = chat
        st.chat_message(role).write(message)
    
    # Step 1: Show main categories
    st.session_state.chat_history.append(("assistant", "Choose a category:"))
    st.chat_message("assistant").write("Choose a category:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Query related to Farming"):
            st.session_state.selected_category = "farming"
    with col2:
        if st.button("🌾 Query related to AgriVision"):
            st.session_state.selected_category = "agrivision"
    
    # Farming Queries (Sub-category selection)
    if st.session_state.get("selected_category") == "farming":
        st.session_state.chat_history.append(("assistant", "Select a sub-category:"))
        st.chat_message("assistant").write("Select a sub-category:")
        
        subcategories = {
            "Crop Selection & Cultivation": "farming_question_1",
            "Irrigation & Water Management": "farming_question_2",
            "Soil & Fertilizer Info": "farming_question_3",
            "Machinery & Equipment": "farming_question_4",
            "Sustainable & Organic Farming": "farming_question_5"
        }
        
        for label, step in subcategories.items():
            if st.button(label):
                st.session_state.selected_subcategory = step
    
    # Farming Questions
    farming_questions = {
        "farming_question_1": ["Best crop for soil?", "Increase yield?", "Ideal planting time?"],
        "farming_question_2": ["Water needs?", "Best irrigation method?", "Water conservation tips?"],
        "farming_question_3": ["Check soil nutrients?", "Ideal pH?", "Fertilization frequency?"],
        "farming_question_4": ["Best small farm tractor?", "Equipment maintenance?", "Latest tech?"],
        "farming_question_5": ["Organic farming?", "Crop rotation benefits?", "Making compost naturally?"]
    }
    
    if st.session_state.get("selected_subcategory") in farming_questions:
        st.session_state.chat_history.append(("assistant", "Select a question:"))
        st.chat_message("assistant").write("Select a question:")
        
        for question in farming_questions[st.session_state.selected_subcategory]:
            if st.button(question):
                st.session_state.chat_history.append(("user", question))
                answers = {
                    "Best crop for soil?": "Conduct a soil test and choose crops suited to its pH and nutrients.",
                    "Increase yield?": "Use high-quality seeds, correct spacing, fertilizers, and pest control.",
                    "Ideal planting time?": "Depends on climate and season; refer to agricultural guidelines.",
                    "Water needs?": "On average, crops need 1-2 inches of water per week.",
                    "Best irrigation method?": "Drip irrigation is most efficient; sprinklers work for larger fields.",
                    "Water conservation tips?": "Use mulch, rainwater harvesting, and efficient irrigation systems.",
                    "Check soil nutrients?": "Use soil test kits or consult agricultural experts.",
                    "Ideal pH?": "Most crops grow well in pH 6.0-7.5.",
                    "Fertilization frequency?": "Depends on the crop type and soil condition.",
                    "Best small farm tractor?": "Compact tractors are ideal for small-scale farming.",
                    "Equipment maintenance?": "Regular cleaning, lubrication, and timely servicing.",
                    "Latest tech?": "AI-powered monitoring, IoT sensors, and smart irrigation.",
                    "Organic farming?": "Gradually switch to organic fertilizers and natural pest control.",
                    "Crop rotation benefits?": "Prevents soil depletion, reduces pests, and increases yield.",
                    "Making compost naturally?": "Use kitchen scraps, dry leaves, and manure for organic compost."
                }
                st.session_state.chat_history.append(("assistant", answers[question]))
                st.chat_message("assistant").write(answers[question])
                st.session_state.selected_category = None
                st.session_state.selected_subcategory = None
    
    # AgriVision Queries
    agrivision_questions = {
        "How can AI help farmers?": "AI helps farmers by analyzing soil data, predicting weather patterns, and automating irrigation.",
        "Latest AgriTech trends?": "Latest trends include AI-powered farming, IoT-based monitoring, and vertical farming.",
        "How does smart irrigation work?": "Smart irrigation uses sensors and AI to optimize water use, reducing waste and increasing crop yield.",
        "What is precision agriculture?": "Precision agriculture involves using GPS, AI, and IoT for accurate farming decisions.",
        "How can drones be used in farming?": "Drones help monitor crop health, detect diseases, and optimize spraying with minimal waste."
    }
    
    if st.session_state.get("selected_category") == "agrivision":
        st.session_state.chat_history.append(("assistant", "Choose a question about AgriVision:"))
        st.chat_message("assistant").write("Choose a question about AgriVision:")
        
        for question, answer in agrivision_questions.items():
            if st.button(question):
                st.session_state.chat_history.append(("user", question))
                st.session_state.chat_history.append(("assistant", answer))
                st.chat_message("assistant").write(answer)
                st.session_state.selected_category = None
                st.session_state.selected_subcategory = None

if __name__ == "__main__":
    main()