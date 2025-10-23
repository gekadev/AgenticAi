from configparser import ConfigParser


class Config : 
    def __init__(self,config_file = './src/langgraphagenticAi/ui/uiConfigFile.ini'):

        self.config = ConfigParser()
        self.config.read(config_file)
    #start read each paramaters 
    def get_llm_options(self):
        return self.config['DEFAULT'].get('LLM_OPTIONS').split(', ') 
    
    #get llm use case 
    def get_usecase_options(self):
        return self.config['DEFAULT'].get('USECASE_OPTIONS').split(', ')
    # get groq model options
    def get_groq_model_options(self):
        return self.config['DEFAULT'].get('GROQ_MODEL_OPTIONS').split(', ')
    
    #get page tite
    def get_page_title(self):
        return self.config['DEFAULT'].get('PAGE_TITLE')
    

 
