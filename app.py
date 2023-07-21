import os
import gradio as gr

from ai_agents import initialize_agent_with_new_openai_functions
from ai_tools import ats_tools
from consts import logs_folder


logs_folder = logs_folder
os.makedirs(logs_folder,exist_ok=True)


def save_logs(chat_history):
    file_path = f"{logs_folder}conversation_logs.txt"
    with open(file_path, 'a') as file:
        for message, response in chat_history:
            file.write(f"User    : {message}\n")
            file.write(f"ATS  : {response} \n")
            file.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            file.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            file.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")



agent = initialize_agent_with_new_openai_functions(tools = ats_tools)
print("\nWelcome to Our Private Applicants Tracking System?")



with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button('Clear')

    def respond(message, chat_history):
        
        result = agent({"input": message})
        answer = result["output"]

        chat_history.append((message, answer))
        save_logs(chat_history)
        return "", chat_history
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    clear.click(lambda: None, None, chatbot, queue = False)

demo.launch(share = True)