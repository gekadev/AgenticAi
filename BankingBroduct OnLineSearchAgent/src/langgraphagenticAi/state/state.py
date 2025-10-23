
from typing_extensions import TypedDict 
from typing import Literal,List,Sequence
from typing import Annotated
import operator
from langgraph.graph.message import add_messages




class State(TypedDict):

    """
       reprsent the struture of staet used in the graph
    """
    messages:Annotated[list,add_messages]
