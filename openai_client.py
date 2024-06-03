from dotenv import load_dotenv
import openai

class OpenAIClient:
    def __init__(self, model, setup_instructions):
        load_dotenv(override=True)
        self.client = openai.OpenAI()
        self.model = model
        self.setup_instructions = setup_instructions

    def get_response(self, prompt):
        messages = [
            {"role": "system", "content": self.setup_instructions},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

    def generate_mcq_question(self, content, difficulty):
        prompt = f"""You are given a file filled with educational content. Your task is to generate one {difficulty} question related to the content. The question must be a Multiple-Choice Question (MCQ). The question should be directly related to the content provided and not include information outside its scope.

                please follow this format:
                
                Question:
                
                    A) Option A
                    B) Option B
                    C) Option C
                    D) Option D
                
                Here is the educational content:
                
                {content}
                
                Based on the content provided, generate an appropriate {difficulty} question without providing the solution."""
        return self.get_response(prompt)

    def generate_code_tracing_question(self, content, difficulty):
        prompt = f"""You are given a file filled with educational content. Your task is to generate one {difficulty} question related to the content. The question should be a Code Tracing and Correction question. The question should be directly related to the content provided and not include information outside its scope.
                provide a code snippet and ask the student to either identify an existing error or bug in the code, or identify the output and the purpose of the code snippet.
            
                Here is the educational content:
                
                {content}
                
                Based on the content provided, generate an appropriate {difficulty} question asking the student a single task without providing the solution."""
        return self.get_response(prompt)

    def generate_code_completion_question(self, content, difficulty):
        prompt = f"""You are given a file filled with educational content. Your task is to generate one {difficulty} question related to the content. The question should be a Code Completion question. The question should be directly related to the content provided and not include information outside its scope.
                provide a partial code snippet and ask the student to complete the missing parts or functionalities of the code.
                
                Here is the educational content:
                
                {content}
                
                Based on the content provided, generate an appropriate {difficulty} question asking the student to complete the code without providing the solution."""
        return self.get_response(prompt)

    def question_generator(self, content, question_type, difficulty):
        if question_type == "Multiple-Choice Questions":
            return self.generate_mcq_question(content, difficulty)
        elif question_type == "Code Tracing and Correction":
            return self.generate_code_tracing_question(content, difficulty)
        elif question_type == "Code Completion":
            return self.generate_code_completion_question(content, difficulty)
        else:
            raise ValueError("Unsupported question type")

    def get_model_feedback(self, question, user_response):
        prompt = f"""You are a helpful teacher's assistant that provides feedback and corrections for student answers. Given a question and a student's answer, provide a concise explanation and correction if necessary. Ensure that your response is clear, easy to understand, and stays within the scope of the question.

                Question: {question}
                Student's Answer: {user_response}
                
                Start your response to the student by stating whether the answer provided is correct or incorrect. Then, follow up with feedback and corrections if necessary.
                """
        return self.get_response(prompt)

    def completion_message(self, content, questions, feedback):
        prompt = f"""Based on the questions asked to a student and the feedback received on their solutions, provide a detailed analysis of the student's skills concerning the content provided. Your response is targeted to the student and should highlight both areas of strength and areas needing improvement to enhance their learning progress.

                Here is the educational content:
                
                {content}
                
                Questions asked to the student:
                
                {', '.join(questions)}
                
                Feedback received on their solutions:
                
                {', '.join(feedback)}
                
                Extract the learning objectives from the provided content. If the student answered a question related to one of the objectives, provide insight and analysis on that. Otherwise, mention that the learning objective was not practiced in this session.
                
                Provide a short and detailed analysis for the student:
                """
        return self.get_response(prompt)