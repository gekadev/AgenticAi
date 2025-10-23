from src.langgraphagenticAi.state.state import State



class BasicChatBotNode :
    def __init__(self,model):
        self.llm = model
   

    def process (self ,state:State)->dict :
        """
         this function is used to process  the input state and generate chatboot responce

        Args:
            state (dict): The current graph state

        Returns:
            str: llm responce 
        """

        return {"messages":self.llm.invoke(state['messages'])}

      
