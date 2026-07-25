import os
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from main import app



st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")

st.title("✈️ AI Travel Planner")

user_query = st.text_input(
    "Enter your travel request",
    placeholder="Example: Plan a 5-day trip to Goa"
)

thread_id = st.text_input("Thread ID", value="user1")

if st.button("Generate Plan"):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    with st.spinner("Generating travel plan..."):

        result = app.invoke(
            {
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": "",
                "llm_calls": 0
            },
            config=config
        )

    st.success("Done!")

    st.subheader("Travel Plan")

    st.write(result["messages"][-1].content)