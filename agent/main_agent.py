from deepagents import create_deep_agent

from agent.llm import llm
from agent.load_prompt import main_config
from agent.sub_agents.db_sub_agent import db_sub_agent
from agent.sub_agents.internet_sub_agent import internet_sub_agent

main_agent = create_deep_agent(
    model=llm,
    system_prompt=main_config["system_prompt"],
    subagents=[db_sub_agent]
)

if __name__ == '__main__':
    result = main_agent.invoke({"messages": [{"role": "user", "content": "列出公司药品的库存列表？"}]})
    print(result["messages"][-1].content)