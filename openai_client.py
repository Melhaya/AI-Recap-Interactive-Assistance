import os
from dotenv import load_dotenv
import openai

# 1. Load .env variables
load_dotenv()  # This will read OPENAI_API_KEY from the .env file

# 2. Assign the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIClient:
    def __init__(self, model, setup_instructions):
        """
        Initializes the OpenAIClient with a specified model and setup instructions.
        """
        load_dotenv(override=True)

        # If you prefer setting the API key here directly from env:
        # openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_DEFAULT_KEY")

        # The new openai>=1.0.0 usage no longer supports openai.OpenAI(), so we directly use openai
        self.model = model
        self.setup_instructions = setup_instructions

    def get_response(self, prompt, temperature=0.7, max_tokens=150, frequency_penalty=0.0):
        """
        Generic chat completion request using OpenAI ChatCompletion.
        """
        messages = [
            {"role": "system", "content": self.setup_instructions},
            {"role": "user", "content": prompt}
        ]
        response = openai.chat.completions.create(model=self.model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty)
        return response.choices[0].message.content

    def generate_mcq_question(self, content, difficulty, questions_asked, **kwargs):
        """
        Generate one MCQ question based on the given content and difficulty.
        """
        prompt = f"""You are given a file filled with educational content. Your task is to generate one {difficulty} question related to the content. The question must be a Multiple-Choice Question (MCQ). The question should be directly related to the content provided and not include information outside its scope.

                please follow this format:
                
                Question:
                
                    A) Option A
                    B) Option B
                    C) Option C
                    D) Option D
                
                Here is the educational content:
                
                {content}
                
                Based on the content provided, generate an appropriate {difficulty} question without providing the solution.
                                
                Do not repeat any of the following questions: 
                
                {questions_asked}
                """
        return self.get_response(prompt)

    def generate_code_tracing_question(self, content, difficulty, questions_asked, **kwargs):
        """
        Generate one Code Tracing and Correction question.
        """
        prompt = f"""You are given a file filled with educational content. Your task is to generate one {difficulty} question related to the content. The question should be a Code Tracing and Correction question. The question should be directly related to the content provided and not include information outside its scope.
                provide a code snippet and ask the student to either identify an existing error or bug in the code, or identify the output and the purpose of the code snippet.
            
                Here is the educational content:
                
                {content}
                
                Based on the content provided, generate an appropriate {difficulty} question asking the student a single task without providing the solution.
                                
                Do not repeat any of the following questions: 
                
                {questions_asked}
                """
        return self.get_response(prompt)

    def generate_code_completion_question(self, content, difficulty, questions_asked, **kwargs):
        """
        Generate one Code Completion question.
        """
        prompt = f"""You are given a file filled with educational content. Your task is to generate one {difficulty} question related to the content. The question should be a Code Completion question. The question should be directly related to the content provided and not include information outside its scope.
                provide a partial code snippet and ask the student to complete the missing parts or functionalities of the code.
                
                Here is the educational content:
                
                {content}
                
                Based on the content provided, generate an appropriate {difficulty} question asking the student to complete the code without providing the solution.
                
                Do not repeat any of the following questions: 
                
                {questions_asked}
                """
        return self.get_response(prompt)

    def question_generator(self, content, question_type, difficulty, questions_asked, **kwargs):
        """
        Delegates question generation to the appropriate method.
        """
        if question_type == "Multiple-Choice Questions":
            return self.generate_mcq_question(content, difficulty, questions_asked, **kwargs)
        elif question_type == "Code Tracing and Correction":
            return self.generate_code_tracing_question(content, difficulty, questions_asked, **kwargs)
        elif question_type == "Code Completion":
            return self.generate_code_completion_question(content, difficulty, questions_asked, **kwargs)
        else:
            raise ValueError("Unsupported question type")

    def get_model_feedback(self, question, user_response, **kwargs):
        """
        Generates feedback for a student's answer using ChatCompletion.
        """
        prompt = f"""You are a helpful teacher's assistant that provides feedback and corrections for student answers. 
Given a question and a student's answer, provide a concise explanation and correction if necessary. 
Ensure that your response is clear, easy to understand, and stays within the scope of the question.

                Question: {question}
                Student's Answer: {user_response}
                
                Start your response to the student by stating whether the answer provided is correct or incorrect. Then, follow up with feedback and corrections if necessary.
                """
        return self.get_response(prompt)

    def completion_message(self, content, questions, feedback, **kwargs):
        """
        Provides a final summary/analysis of the student's performance.
        """
        student_progress = str(dict(zip(questions, feedback)))

        prompt = f"""Based on the questions asked to a student and the feedback received on their solutions, 
provide a detailed analysis of the student's skills concerning the content provided. 
Your response is targeted to the student and should highlight both areas of strength and areas needing improvement 
to enhance their learning progress.

Here is the educational content:
{content}

Questions asked to the student and the feedback received:
{student_progress}

Extract the learning objectives from the provided content. If the student answered a question related to 
one of the objectives, provide insight and analysis on that. Otherwise, mention that the learning objective was not practiced in this session.

Provide a short and detailed analysis for the student. Response Structure:

1. Learning Objectives:
    • List objectives and note if they were practiced with insights.
2. Performance Analysis:
    • Strengths: [Key strengths]
    • Improvements: [Areas for improvement with suggestions]
3. Recommendations:
    • [Actionable steps for improvement]
"""
        return self.get_response(prompt, **kwargs)