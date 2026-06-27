from pathlib import Path

from pdf_service import read_pdf
from prompt_service import build_resume_prompt
from llm_service import ask_llm


def main():
    resume_path = Path("resumes/resume.pdf")

    resume_text = read_pdf(resume_path)

    prompt = build_resume_prompt(resume_text, "Can this candidate fit a full stack developer role?")
    
    answer = ask_llm(prompt=prompt)
    
    print(answer)


if __name__ == "__main__":
    main()