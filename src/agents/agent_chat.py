from typing import AsyncGenerator
from src.utils import OPENAI_API_KEY
from llama_index.core.agent import FunctionAgent, AgentStream
from llama_index.core.workflow import Context
from llama_index.llms.openai import OpenAI
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec



async def create_chat_agent(chat_message: str) -> AsyncGenerator[str, str]:
  tool_spec = YahooFinanceToolSpec()

  workflow = FunctionAgent(
    name="bullens-agent",
    description="A chat agent for the Bullens application",
    system_prompt = (
      "You are a helpful assistant for the Bullens application. "
      "You must answer any user question as long as it is related to stocks, including listing, comparing, or analyzing stocks. "
      "All data and answers must be sourced from Yahoo Finance. Do not answer questions unrelated to stocks."
    ),
    tools=tool_spec.to_tool_list(),
    llm=OpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY, streaming=True),
  )

  ctx = Context(workflow=workflow)

  agents = workflow.run(user_msg=chat_message, context=ctx)

  async for events in agents.stream_events():
    if isinstance(events, AgentStream):
      yield events.delta
