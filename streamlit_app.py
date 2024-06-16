from weaviate_cluster.client.client import connect_to_cluster_as_streamlit
import streamlit as st
import time


from dotenv import load_dotenv

from weaviate_cluster.query.query_near_text import query_ai_solutions

# Note: This file must be executed using the Streamlit executable!

load_dotenv()

st.set_page_config(
    page_title='QAware: AI Chatbot',
    layout="wide",
    initial_sidebar_state="expanded",
)


def display_chat_messages() -> None:
    """Print message history
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Title
st.title("QAware @ Cloudland 2024")

# we want to align the chat to the right of the robot background, so we create everything in the right column.
_, col2 = st.columns(2)

with col2:
    # .stChatMessage {
    #     background: rgba(255,255,255,0.8)
    # }

    # Set the background image
    background_image = """
    <style>
    
    [data-testid="stAppViewContainer"] > .main {
        background-image: url('/app/static/galaxy-bot-aiden.webp');
        background-size: contain;
        background-position: center;  
        background-repeat: no-repeat;
    }
    
    </style>
    """
    st.markdown(background_image, unsafe_allow_html=True)

    # Connection to Weaviate thorugh Connector
    conn = connect_to_cluster_as_streamlit()


    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.wasGreeted = False

    # Display chat messages from history on app rerun
    print("Rerunning.")
    display_chat_messages()

    # Greet user
    if not st.session_state.wasGreeted:
        with st.chat_message("assistant"):
            intro = "Hallo! Ich bin der AI-Chatbot von QAware, Ihr Assistent bei der Suche nach der besten Lösung für Ihr AI-Problem. Los geht's!"
            st.markdown(intro)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": intro})
            st.session_state.wasGreeted = True

    # Example prompts
    example_prompts = [
        "Wir haben einen AI Prototypen gebaut, stecken fest und kommen nicht weiter.",
        "Wie können wir die Integration unserer AI Produkte verbessern?",
        "Wie kann ich AI in meinem Unternehmen erfolgreich einführen?",
        "Habe ich die richtigen Daten um meine AI Use Cases umzusetzen?",
        "Die Produktiviät und Effizienz meiner Teams ist nicht so hoch, wie ich es mir wünsche.",
        "Wie kann ich ein schnelles Kunden-Feedback zu meiner Idee bekommen?",
    ]

    example_prompts_mouseover = [
        "Wie können wir unseren AI Prototypen weiterentwickeln und verbessern?",
        "Wie könnnen wir den Zugriff auf Daten und Prozesse zur Automatisierung in unsere IT-Systemen in unserer Anwendungslandschaft verbessern?",
        "Welche Use Cases sind für mein Unternehmen geeignet? Habe ich die notwendigen Voraussetzungen für AI?",
        "Wie kann ich eine professionelle Betriebsumgebung und professionellen Betrieb aufbauen?",
        "Meine Data Scientists, Data Analysts und AI Engineers haben Schwierigkeiten, ihre AI Modelle in Produktion zu bringen",
        "Wie kann ich Klarheit zu meiner AI Idee gewinnen und einen Business Case validieren?",
    ]

    buttons = list(zip(example_prompts, example_prompts_mouseover))
    rows = [st.columns(3), st.columns(3)]

    button_pressed = ""

    # Display buttons and check for clicks
    for i, (prompt, help_text) in enumerate(buttons):
        if rows[i // 3][i % 3].button(prompt, help=help_text):
            button_pressed = prompt

    if prompt := (st.chat_input("Vor welchen AI Herausforderungen steht Ihr Unternehmen?") or button_pressed):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        prompt = prompt.replace('"', "").replace("'", "")

        if prompt != "":
            # query_talks_and_ai_solutions(prompt)
            first_ai_solution = query_ai_solutions(prompt)

            response = ""
            with st.chat_message("assistant"):

                first_result = first_ai_solution

                if first_result.metadata.certainty > 0.9:
                    chat_response_intro = """Für Ihren Anwendungsfall empfehlen wir  \n\nunsere **{solution}** Lösung.""".format(solution=first_result.properties['solution'])
                    chat_response_details = first_result.properties['answer']

                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in chat_response_intro.split():
                        # print("chunk is '"+chunk+'"')
                        full_response += chunk + " "
                        time.sleep(0.02)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    response += full_response + " "

                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                    # ================================================
                    response2 = ""

                    message_placeholder = st.empty()

                    full_response = ""
                    for chunk in chat_response_details.split():
                        # print("chunk is '"+chunk+'"')
                        full_response += chunk + " "
                        time.sleep(0.02)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    response2 += full_response + " "

                    st.link_button(label="Weitere Details", url=first_result.properties["link"])

                    st.session_state.messages.append(
                        {"role": "assistant", "content": response2}
                    )
                else:
                    message_placeholder = st.empty()
                    assistant_response = "Könntest du uns etwas mehr Informationen geben, um das Problem zu beschreiben?"
                    full_response = ""
                    for chunk in assistant_response.split():
                        # print("chunk is '"+chunk+'"')
                        full_response += chunk + " "
                        time.sleep(0.02)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    response += full_response + " "

                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

