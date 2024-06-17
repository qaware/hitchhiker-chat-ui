import streamlit as st
import time


from dotenv import load_dotenv

from weaviate_cluster.query.query_near_text import query_ai_solutions, query_talks

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
            for line in message["content"]:
                st.markdown(line)

def proc():
    st.session_state.mode = mode
    st.session_state.messages = []

with st.sidebar:
    mode = st.radio(
        "Antworten zu...", options=["Cloudland", "QAware AI Lösungen"], index=0,
        on_change=proc
    )

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

    # Initialize chat history
    if "messages" not in st.session_state or st.session_state.messages == []:
        st.session_state.messages = []
        if mode == "QAware AI Lösungen":
            st.session_state.messages.append({"role": "assistant", "content": ["Hallo! Ich bin der AI-Chatbot von QAware, Ihr Assistent bei der Suche nach der besten Lösung für Ihr AI-Problem. Los geht's!"]})
        else:
            st.session_state.messages.append({"role": "assistant", "content": ["Hallo! Ich bin der AI-Chatbot von QAware und kann Ihnen Talks auf der Cloudland empfehlen."]})
    # Display chat messages from history on app rerun
    display_chat_messages()

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

    if mode == "QAware AI Lösungen":
        # Display buttons and check for clicks
        for i, (prompt, help_text) in enumerate(buttons):
            if rows[i // 3][i % 3].button(prompt, help=help_text):
                button_pressed = prompt
        text = "Vor welchen AI Herausforderungen steht Ihr Unternehmen?"
    else:
        text = "Für welche Themenbereiche interessieren Sie sich auf der Cloudland?"

    if prompt := (st.chat_input(text) or button_pressed):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": [prompt]})

        prompt = prompt.replace('"', "").replace("'", "")

        if prompt != "" and mode == "QAware AI Lösungen":
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
                        full_response += chunk + " "
                        time.sleep(0.02)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    response += full_response + " "

                    st.session_state.messages.append(
                        {"role": "assistant", "content": [response]}
                    )
                    # ================================================
                    response2 = ""

                    message_placeholder = st.empty()

                    full_response = ""
                    for chunk in chat_response_details.split():
                        full_response += chunk + " "
                        time.sleep(0.02)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    response2 += full_response + " "

                    st.link_button(label="Weitere Details", url=first_result.properties["link"])

                    st.session_state.messages.append(
                        {"role": "assistant", "content": [response2]}
                    )
                else:
                    message_placeholder = st.empty()
                    assistant_response = "Könntest du uns etwas mehr Informationen geben, um das Problem zu beschreiben?"
                    full_response = ""
                    for chunk in assistant_response.split():
                        full_response += chunk + " "
                        time.sleep(0.02)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    response += full_response + " "

                    st.session_state.messages.append(
                        {"role": "assistant", "content": [response]}
                    )
        # Cloudland questions
        else:
            # query_talks_and_ai_solutions(prompt)
            results = query_talks(prompt)

            response = ""
            with st.chat_message("assistant"):
                chat_response = "Die Top 3 relevantesten Talks dazu sind:"
                for result in results:
                    talk = result.properties

                    template = """===========================
                    **{title}**
                    Speaker: {speaker} ({company})
                    Wann & Wo: {time}
                    Abstract: {abstract}
                    """.format(title=talk['title'], speaker=talk['speaker'], company=talk['company'].replace("\n", ""), time=talk['time'], abstract=talk['abstract'].replace("\n", ""))

                    chat_response += "\n" + template

                for line in chat_response.splitlines(keepends=True):
                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in line.split():
                        full_response += chunk + " "
                        time.sleep(0.02)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)
                    response += full_response + " "
                    st.session_state.messages.append(
                        {"role": "assistant", "content": [response]}
                    )


