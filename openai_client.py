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

    def generate_question(self, content):
        prompt = f"""You are given a file filled with educational content. Your task is to generate one question related to the content. The question can be either a Multiple-Choice Question (MCQ) or a Code Tracing and Correction question. The question should be directly related to the content provided and not include information outside its scope.

                If you choose to generate an MCQ, please follow this format:
                
                Question:
                
                    A) Option A
                    B) Option B
                    C) Option C
                    D) Option D
                
                If you choose to generate a Code Tracing and Correction question, provide a code snippet and ask the student to either identify an existing error or bug in the code, or identify the output and the purpose of the code snippet.
                
                Here is the educational content:
                
                {content}
                
                Based on the content provided, generate an appropriate question."""
        return self.get_response(prompt)

    def get_model_feedback(self, question, user_response):
        prompt = f"""You are a helpful teacher's assistant that provides feedback and correction for student answers. Given a question and a student's answer, provide a concise explanation and correction if necessary. Ensure that your response is clear, easy to understand, and stays within the scope of the question.

                Question: {question}
                Student's Answer: {user_response}
                
                Feedback and correction:
                """
        return self.get_response(prompt)