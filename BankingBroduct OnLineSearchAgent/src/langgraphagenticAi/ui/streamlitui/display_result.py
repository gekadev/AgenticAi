
import re        
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage




#class DisplayResultStreamlit:
    # def __init__(self, usecase, graph, user_message):
    #     self.usecase = usecase
    #     self.graph = graph
    #     self.user_message = user_message

    # def display_result_on_ui(self):
    #     usecase = self.usecase
    #     graph = self.graph
    #     user_message = self.user_message

    #     if usecase == "Basic Chatbot":
    #         # Display user message once
    #         with st.chat_message("user"):
    #             st.write(user_message)
                

    #         # Display assistant responses
    #         assistant_responses = []
    #         for event in graph.stream({"messages": ("user", user_message)}):
    #             for value in event.values():
    #                 msg = value["messages"]
    #                 content = msg.content if hasattr(msg, "content") else str(msg)
    #                 clean_content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    #                 assistant_responses.append(clean_content)

    #         # Render assistant message once after streaming
    #         with st.chat_message("assistant"):
    #             for res in assistant_responses:
    #                 st.write(res)


    ##this is real code
# import re        
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        

        if usecase == "Basic Chatbot":
            # --- Initialize session history ---
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            # --- Add new user message to history ---
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            print(user_message)

            # --- Display previous chat history ---
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            # --- Stream assistant response ---
            assistant_message = ""
            for event in graph.stream({"messages": ("user", user_message)}):
                for value in event.values():
                    print(value['messages'])
                    print(event.values())
                    msg = value.get("messages", "")
                    if isinstance(msg, BaseMessage):
                        msg = [msg]

                    for m in msg:
                        content = getattr(m, "content", str(m))
                        clean_content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
                        if clean_content:
                            assistant_message = clean_content

            # --- Save assistant message to session history ---
            if assistant_message:
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_message})

            # --- Display assistant message ---
            with st.chat_message("assistant"):
                st.write(assistant_message)
                
        elif usecase=="Chatbot With Web":
             # Prepare state and invoke the graph
            initial_state = {"messages": [user_message]}
            res = graph.invoke(initial_state)
            for message in res['messages']:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
        
                elif type(message)==AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)


        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news... ⏳"):
                result = graph.invoke({"messages": frequency})

                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    # Display the markdown content in Streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")                        
