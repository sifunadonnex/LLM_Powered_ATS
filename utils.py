# I have got 600 pdfs, I wanna read them one by one using an llm agaent , it scores the pdf content based on some rules and then retruns a csv with a name column and overall score
# But since an llm has a context length limit it should do this one by one, in such a way each pdf is treated as one independent iteration. Also i need one function to calaculate the number of tokens, if tokens are
# more than 8096, I summarize the text to that exact 8096 tokens so That it fits in that token context limit

import os
import csv
import PyPDF2
import openai
from dotenv import load_dotenv, find_dotenv
from consts import gpt_model

#load our open ai api key
_ = load_dotenv(find_dotenv())

openai.api_key = os.environ['OPENAI_API_KEY']


#get completion logic and token count
def get_completion(prompt, model=gpt_model):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0 # this is the degree of randomness of the model's output,
        
    )
    content = response.choices[0].message["content"]
    token_dict = {
        'prompt_tokens':response['usage']['prompt_tokens'],
        'completion_tokens': response['usage']['completion_tokens'],
        'total_tokens': response['usage']['total_tokens'],
                                    
    }    
    return content, token_dict



#score pdf based on an llm agent
def score_pdf(pdf_content, prompt):
    try:
        #here you define the ruless of how you wanna track the applicants
        prompt_template = f"""
            You are an Intelligent Applicants Tracking System. You are supposed to be a helping hand to HR personell, to screen multiple applicants based on  requirements
            provided by the HR personell :

            Here are the HR requirements provided by the HR enclosed in back ticks:
            ```{prompt}'''

            this is the pdf content you are supposed to rank enclosed in dollar signs
            $$${pdf_content}$$$

            These are the rules you are supposed to use in ranking enclosed in % signs
            %%% Count the number of requirements, divide 100% by that number, then if the pdf content satisfies the requirement assign that percentage else zero
                Iterate through each requirement then
                Return the output in the below format:
                    overall_score: percentage out of 100
            %%%
                


        """
        # print(prompt_template)
        response, token_dict = get_completion(prompt_template)

        return response, token_dict
    
    except Exception as e:
        return f"An error occurred: {e}"


def process_pdfs(pdf_folder, output_csv_file, prompt):
    try:
        with open(output_csv_file, 'w', newline = '') as csvfile:
            fieldnames = ['Name', 'Result']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()

            for pdf_file in os.listdir(pdf_folder):
                if pdf_file.endswith('.pdf'):
                    pdf_path = os.path.join(pdf_folder, pdf_file)

                    #read the content of the pdf
                    pdf_content = ""
                    with open(pdf_path, "rb") as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        num_pages = len(pdf_reader.pages)
                        
                        for page_number in range(num_pages):
                            page = pdf_reader.pages[page_number]
                            pdf_content += page.extract_text()

                    #check if content exceeds the context length limit and summarize if necessary

                    
                    
                    result , token_count = score_pdf(pdf_content, prompt)

                    print(token_count)

                    #write the results
                    writer.writerow({'Name': pdf_file, 'Result': result})

        return "Done with the ranking, view the Output folder for the results"
    
    except Exception as e:
        return f"This error occurred: {e}" 


if __name__ == '__main__':
    pdf_folder_path ="data"
    output_csv_file_path = "output/results.csv"

    print("\n Welcome to your Applications Tracking System! ")
    while True:

        requirements = input("n\nRequest: ")
        process_pdfs(pdf_folder_path,output_csv_file_path, requirements)


