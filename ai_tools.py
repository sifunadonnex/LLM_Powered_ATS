from utils import process_pdfs
from pydantic import BaseModel, Field
from langchain.tools import tool
from consts import pdf_folder_path,output_csv_file_path

#Pydantic is a data validation and settings management library often used with FastAPI to define requeata and response models for API endpoints
#They help ensure that the incoming data matches the expected structure and types defined in the models.

class RequirementsInput(BaseModel):
    information: str = Field(
        desccription = "rank resumes based on requirements given"
    )





@tool("rank_resumes_based_on_requirements_given", return_direct = True, args_schema= RequirementsInput)
def tool_rank_resumes(information: str) -> str:

    """Given requirements, rank the resumes of applicatants by returning a score for each resume
            
    """

    return process_pdfs(pdf_folder=pdf_folder_path, output_csv_file=output_csv_file_path, prompt=information)


ats_tools = [

    tool_rank_resumes
]