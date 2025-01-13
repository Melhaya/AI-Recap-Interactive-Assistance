import os
from dotenv import load_dotenv
import openai

# 1. Load .env variables
load_dotenv()  # This will read OPENAI_API_KEY from the .env file

class OpenAIClient:
    def __init__(self, model, setup_instructions):
        """
        Initializes the OpenAIClient with a specified model and setup instructions.
        """
        load_dotenv(override=True)

        # If you prefer setting the API key here directly from env:
        # openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_DEFAULT_KEY")

        self.model = model
        self.setup_instructions = setup_instructions

    def get_response(self, prompt, temperature=0.7, max_tokens=150, frequency_penalty=0.0, **kwargs):
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

    def generate_mcq_question(self, content, difficulty, questions_asked, course_objectives, selected_objectives, **kwargs):
        """
        Generate one MCQ question based on the given content and difficulty.
        """
        # Format objectives to show them clearly
        objectives_list_str = "\n".join(f"• {obj}" for obj in course_objectives)
        objectives_str = ", ".join(selected_objectives)
        objective_focus_str = f"The student wants to focus on: {objectives_str}" if selected_objectives else "No specific objective chosen"

        prompt = f"""
        You are given a file filled with educational content. 
        Here are the overall course objectives:
        {objectives_list_str}
        
        {objective_focus_str}
        
        Your task is to generate one {difficulty} Multiple-Choice Question (MCQ).
        It must be directly related to the content provided and not include information outside its scope. 
        The primary objectives to focus on are: {objectives_str}. Ensure your question targets this objective specifically.
        
        Please follow this format:
        
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
        return self.get_response(prompt, **kwargs)

    def generate_code_tracing_question(self, content, difficulty, questions_asked, course_objectives, selected_objectives, **kwargs):
        """
        Generate one Code Tracing and Correction question.
        """
        objectives_list_str = "\n".join(f"• {obj}" for obj in course_objectives)
        objectives_str = ", ".join(selected_objectives)
        objective_focus_str = f"The student wants to focus on: {objectives_str}" if selected_objectives else "No specific objective chosen"

        prompt = f"""
        You are given a file filled with educational content.
        Here are the overall course objectives:
        {objectives_list_str}
        
        {objective_focus_str}
        
        Your task is to generate one {difficulty} Code Tracing and Correction question.
        The question should be directly related to the content provided and not include information outside its scope.
        The primary objectives to focus on are: {objectives_str}. Ensure your question targets this objective specifically.
        
        Provide a code snippet and ask the student to either identify an existing error or bug in the code, 
        or identify the output and the purpose of the code snippet.
        
        Here is the educational content:
        
        {content}
        
        Based on the content provided, generate an appropriate {difficulty} question asking the student a single task 
        without providing the solution.
        
        Do not repeat any of the following questions:
        
        {questions_asked}
        """
        return self.get_response(prompt, **kwargs)

    def generate_code_completion_question(self, content, difficulty, questions_asked, course_objectives, selected_objectives, **kwargs):
        """
        Generate one Code Completion question.
        """
        objectives_list_str = "\n".join(f"• {obj}" for obj in course_objectives)
        objectives_str = ", ".join(selected_objectives)
        objective_focus_str = f"The student wants to focus on: {objectives_str}" if selected_objectives else "No specific objective chosen"

        prompt = f"""
        You are given a file filled with educational content.
        Here are the overall course objectives:
        {objectives_list_str}
        
        {objective_focus_str}
        
        Your task is to generate one {difficulty} Code Completion question.
        The question should be directly related to the content provided and not include information outside its scope.
        The primary objectives to focus on are: {objectives_str}. Ensure your question targets this objective specifically.
        
        Provide a partial code snippet and ask the student to complete the missing parts or functionalities of the code.
        
        Here is the educational content:
        
        {content}
        
        Based on the content provided, generate an appropriate {difficulty} question 
        asking the student to complete the code without providing the solution.
        
        Do not repeat any of the following questions:
        
        {questions_asked}
        """
        return self.get_response(prompt, **kwargs)

    def question_generator(self, content, question_type, difficulty, questions_asked, course_objectives, selected_objectives, **kwargs):
        """
        Delegates question generation to the appropriate method.

        Expecting potential extra kwargs:
          - course_objectives: (List[str])
          - selected_objectives: (str)
        """
        if question_type == "Multiple-Choice Questions":
            return self.generate_mcq_question(content, difficulty, questions_asked,course_objectives, selected_objectives, **kwargs)
        elif question_type == "Code Tracing and Correction":
            return self.generate_code_tracing_question(content, difficulty, questions_asked, course_objectives, selected_objectives, **kwargs)
        elif question_type == "Code Completion":
            return self.generate_code_completion_question(content, difficulty, questions_asked, course_objectives, selected_objectives, **kwargs)
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
        
        Start your response by stating whether the answer provided is correct or incorrect, 
        then follow up with feedback and corrections if necessary.
        """
        return self.get_response(prompt, **kwargs)

    def completion_message(self, content, questions, feedback, course_objectives, selected_objectives, **kwargs):
        """
        Provides a final summary/analysis of the student's performance.
        """
        student_progress = str(dict(zip(questions, feedback)))

        prompt = f"""Based on the questions asked to the student and the feedback received on their solutions, 
        please provide a detailed analysis of the student's skills concerning the content provided. 
        Your response should be addressed to the student and highlight both areas of strength and areas needing improvement 
        to enhance their learning progress.
        
        Here is the educational content:
        {content}
        
        These are the course’s learning objectives:
        {', '.join(course_objectives)}
        
        The student specifically chose to focus on:
        {', '.join(selected_objectives)}
        
        Below are the questions asked and the feedback received:
        {student_progress}
        
        Please address the following:
        
        1. Overall Objectives:
           • For each of the listed objectives above, note if the student practiced it in this session or not.
           • If an objective wasn’t tested in any question, mention that it remains unassessed.
        
        2. Performance Analysis:
           • Strengths: Summarize the key strengths observed in the student's answers.
           • Improvements: Identify any areas needing clarification or correction. 
           • Specific Focus: Discuss the student's performance on their chosen objective(s): “{', '.join(selected_objectives)}.”
        
        3. Recommendations:
           • Provide actionable next steps for the student to improve their understanding and skills, 
             especially regarding their chosen objective(s).
        
        Your response should be addressed to the student
        """
        return self.get_response(prompt, **kwargs)