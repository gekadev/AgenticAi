from click import prompt
from streamlit import chat_message
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import re
import sys ,os,html

# Force stdout (console) to use UTF-8
sys.stdout.reconfigure(encoding='utf-8')

class AINewsNode:
    def __init__(self,llm):
        """
        Initialize the AINewsNode with API keys for Tavily and GROQ.
        """

        self.tavily = TavilyClient()
        self.llm = llm
        # this is used to capture various steps in this file so that later can be use for steps shown
        self.state = {}



    def fetch_news(self,state:dict)->dict:
        """
            Fetch AI news based on the specified frequency.
            
            Args:
                state (dict): The state dictionary containing 'frequency'.
            
            Returns:
                dict: Updated state with 'news_data' key containing fetched news.
        """
        

        frequency = state['messages'][0].content.lower()
        self.state['frequency']=frequency
        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm', 'year': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 366}
        response = self.tavily.search(
                query="latest finanial product in bank like new product in credit card ,loans or  any offer in bank in egypt or globaly",
                #query = "latest banking products and financial offers in Egypt, including new credit cards, personal loans, and digital banking innovations",

              #  query="get latest banking product in egypt and globally",

                topic="finance",
                #topic="news",
                country="united states",
                time_range=time_range_map[frequency],
                include_answer="advanced",
                max_results=10,
                days=days_map[frequency],
                #include_domains=["*.bank.com"]
                # include_domains=["techcrunch.com", "venturebeat.com/ai", ...]  # Uncomment and add domains if needed
            )
        
        state['news_data'] = response.get('results',[])
        self.state['news_data'] = state['news_data']
        
        return state


    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news using an LLM.

        Args:
            state (dict): The state dictionary containing 'news_data'.

        Returns:
            dict: Updated state with 'summary' key containing the summarized news.
        """


        news_items = self.state['news_data']


        # prompt_template = ChatPromptTemplate.from_messages([
        # ("system", """Summarize AI news articles into markdown format. For each item include:
        # - Date in **YYYY-MM-DD** format in IST timezone
        # - Concise sentences summary from latest news
        # - Sort news by date wise (latest first)
        # - Source URL as link
        # Use format:
        # ### [Date]
        # - [Summary]
        # - (URL)"""),
        
        # ("user", "Articles:\n{articles}")
        # ])   


        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a financial research assistant specializing in banking products.
        Summarize the latest announcements, launches, or updates in the **banking sector** — especially
        credit cards, personal loans, digital lending, savings accounts, and fintech innovations.

        Your goal:
        - Focus only on **new or updated banking products or services** (not general finance news).
        - Highlight unique features, benefits, eligibility, or technological innovations (e.g., AI, digital KYC, mobile banking).
        - Convert all dates to **YYYY-MM-DD** format in IST timezone.
        - Sort news items **latest first** (by date).
        - Include the **bank name or financial institution** in the summary.
        - Provide the **source URL** as a hyperlink.
        - Output in clean **Markdown** format as shown below.

        Format example:
        ### [Date]
        - **[Bank Name]** launched a new [Product Type] offering [Key Feature] —
              - [Summary]
              (URL)"""),
        
            ("user", "Articles:\n{articles}")
        ])
  


        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary'] = self.clean_text(response.content)

       # state['summary']  = re.sub(r"<think>.*?</think>", "", state['summary'] , flags=re.DOTALL).strip()

        self.state['summary'] = state['summary']
        return self.state


    def save_result(self,state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        
       # summary = re.sub(r"<think>.*?</think>", "", summary, flags=re.DOTALL).strip()

        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w' ,encoding="utf-8") as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state


    def clean_text(self,text: str) -> str:
        """Fix encoding and remove non-English characters from text."""
        if not text:
            return ""

        # Step 1: Decode mojibake (wrongly decoded UTF-8)
        try:
            text = text.encode('latin1').decode('utf-8')
        except Exception:
            pass

        # Step 2: Convert HTML entities like &amp; or &#39; to characters
        text = html.unescape(text)
        # Step 4: Remove any remaining non-English characters (anything outside ASCII)
        text = re.sub(r"[^\x00-\x7F]+", " ", text)

        # Step 5: Collapse extra spaces
        #text = re.sub(r"\s+", " ", text).strip()
        return text



   

     # prompt_template = ChatPromptTemplate.from_messages([
        #     ("system", """You are a financial research assistant specializing in banking products.
        # Summarize the latest announcements, launches, or updates in the **banking sector** — especially
        # credit cards, personal loans, digital lending, savings accounts, and fintech innovations.

        # Your goal:
        # - Focus only on **new or updated banking products or services** (not general finance news).
        # - Highlight unique features, benefits, eligibility, or technological innovations (e.g., AI, digital KYC, mobile banking).
        # - Convert all dates to **YYYY-MM-DD** format in IST timezone.
        # - Sort news items **latest first** (by date).
        # - Include the **bank name or financial institution** in the summary.
        # - Provide the **source URL** as a hyperlink.
        # - Output in clean **Markdown** format as shown below.

        # Format example:
        # ### [Date]
        # - **[Bank Name]** launched a new [Product Type] offering [Key Feature] —
        #       [Summary](URL)"""),
        
        #     ("user", "Articles:\n{articles}")
        # ])
