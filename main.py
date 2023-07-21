from ai_agents import initialize_agent_with_new_openai_functions
from ai_tools import ats_tools

#initialize tools



agent = initialize_agent_with_new_openai_functions(tools = ats_tools)
print("\nWelcome to Our Private ATS tool?")

while True:
    request = input("n\nRequest: ")
    result = agent({"input": request})
    answer = result["output"]

    print(answer)

