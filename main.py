import streamlit as st
from agent import initialize_ai_model, create_ai_crew, generate_itinerary
from tools import load_api_key, search_tool

def main():
   
    st.set_page_config(
        page_title="Travel Planner-Anifa",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("""
        <style>

        h1 {
            color: #4b4b4b;
            text-align: center;
            padding: 15px 0;
        }
        
        </style>
        """, unsafe_allow_html=True)
    
    st.title("    ✈️ Travel Planner    ")


    # Mengajukan pertanyaan kepada pengguna
    origin = st.text_input("🏠 From where will you be traveling from?")
    cities = st.text_input("🛬 What are the cities options you are interested in visiting? (separate by commas)")
    date_range = st.text_input("📅 What is the date range you are interested in traveling?")
    interests = st.text_input("🎨 What are some of your high level interests and hobbies?")

    if st.button("Generate Itinerary"):
        #Load API key from environtment
        api_key = load_api_key()
        if not api_key:
            st.error("API key not found. Please set your API")
            return
        #Initialize AI model 
        openaigpt4 = initialize_ai_model(api_key)

        # Data yang akan diproses oleh AI Crew
        data = {
            "origin": origin,
            "cities": cities,
            "date_range": date_range,
            "interests": interests
        }


        # Create AI Crew
        ai_crew = create_ai_crew(openaigpt4)

        #Generate Itinerary
        itinerary = generate_itinerary(data, ai_crew)

        #Display Itinerary
        st.subheader ("AI-Generated Itinerary")
        st.markdown(itinerary)

        #Search DuckDuckGo dengan data yang sama
        search_query = f"{origin} {cities} {date_range} {interests}"
       
        try:
            search_results = search_tool.run(tool_input=search_query)
            
            # Check if search results are string or list
            if isinstance(search_results, str):
                # Print the raw search results as a string
                st.subheader("Other Recomendation :")
                results_list = search_results.split('\n')  # Memisahkan hasil berdasarkan baris baru
                for result in results_list:
                    st.write(result)    

            elif isinstance(search_results, list):
                # Print search results assuming it's a list of dictionaries
                st.subheader("DuckDuckGo Search Results:")
                for result in search_results:
                    st.write(f"**{result.get('title', 'No Title')}**")
                    st.write(result.get('href', 'No URL'))
                    st.write(result.get('body', 'No Body'))
            else:
                st.write("Unexpected search results format.")
        except Exception as e:
            st.error(f"An error occurred while searching: {e}")
        
    
if __name__ == "__main__":
    main()
