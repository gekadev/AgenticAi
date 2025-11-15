from langsmith import expect
import streamlit as st
from src.ui.streamlitui.loadui import LoadStreamlitUI
from src.llms.groqllm import GroqLLM
from src.llms.geminillm import GeminiLLM
from src.graphs.graph_builder import GraphBuilder
from src.ui.streamlitui.display_result import  DisplayResultStreamlit




def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.

    """

    ##Load UI
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    user_message = st.chat_input("Enter your message:")

    if user_message :
        try :
            #load llm
             gem_llm  =GeminiLLM()
             model = gem_llm.get_llm()

             #llm_object_config=GroqLLM()

            # model = llm_object_config.get_llm()
             if not model :
                 st.error('Error: LLM model could not be initialized')
                 return
             # inistialize and sert up graphe  based on use cases
             usecase = user_input.get('selected_usecase')
             if not usecase : 
                 st.error ('Error: No use case selected.')    

             # start Graph builder
             graph_builder = GraphBuilder(model)
             try :
                  graph =graph_builder.setup_graph(usecase)
                  DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
             except Exception as e :
                   st.error(f"Error: Graph set 2up failed- {e}")
                   return

        except Exception as e :
             st.error(f"Error: Graph set up failed- {e}")
             return   
