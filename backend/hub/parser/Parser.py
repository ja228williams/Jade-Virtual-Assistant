from apps.ReqFormat.FuncWrap import FuncWrap
from apps.ReqFormat.ReqFormat import ReqFormat

# from sentence_transformers import SentenceTransformer, util

from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage


# parser for the hub
class Parser:
    def __init__(self, hub):
        self.req_format_cache = {}
        self.hub = hub
        # self.req_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
        print('parser initialized')

    def parse(self, msg, app):
        """
        Parses msg and determines how to handle msg request.

        :param msg: raw string message
        :param app: name of app the message is directed towards
        :return: function identified corresponding to msg and app (or None if not necessary), response message for the app
        """
        tools = self.hub.retrieve_func_tools(app)
        open_ai_agent = initialize_agent(tools=tools, llm=self.llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
        resp = open_ai_agent.run(msg)
        return resp
