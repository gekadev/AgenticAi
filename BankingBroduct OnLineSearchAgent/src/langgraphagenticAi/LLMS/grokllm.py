import os
import streamlit as st
from langchain_groq import ChatGroq

# start bulding our class for grok model
class GrokLLM:
    """
    this class is used for grok llm model initialization

    """

    def __init__(self,user_controls_input):
        """_

        Args:
            user_controls_input (string): 
            this used to pass grok llm api key from fromt enf from session
        """
   
        self.user_controls_input = user_controls_input


    def get_llm_model(self):
        """_summary_
        load all ai model model name , api key

        Returns:
            _type_: llm model 
        """

        try:
            #get key 
            groq_api_key = self.user_controls_input['GROQ_API_KEY']
            selected_groq_model = self.user_controls_input['selected_groq_model']
            if groq_api_key=='' and os.environ['GROQ_API_KEY'] == '':
                st.error('Please Enter Your Groq api key')
            llm=ChatGroq(api_key=groq_api_key,model=selected_groq_model)

        except Exception as e:
            raise ValueError(f'Error occuerd with Exception : {e}')    

        return llm    
