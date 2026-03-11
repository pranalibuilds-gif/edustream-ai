import ollama
import json
import re

class LLMEngine:
    """
    Advanced LLM Engine with Multi-Language support and recursive summarization.
    """

    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.chunk_size = 10000 

    def _chunk_text(self, text: str):
        """
        Splits text into chunks to stay within context limits.
        """
        return [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]

    def generate_summary(self, transcript: str, target_lang: str = "English") -> str:
        """
        Generates a summary in the specified target language.
        """
        chunks = self._chunk_text(transcript)
        
        if len(chunks) == 1:
            return self._run_summary_prompt(chunks[0], target_lang=target_lang)
        
        mini_summaries = []
        for i, chunk in enumerate(chunks):
            # Tell the AI to summarize this specific part in the target language
            chunk_prompt = f"Summarize this part ({i+1}/{len(chunks)}) of the lecture in {target_lang}: {chunk}"
            try:
                response = ollama.generate(model=self.model_name, prompt=chunk_prompt)
                mini_summaries.append(response['response'])
            except:
                continue
        
        combined_context = "\n\n".join(mini_summaries)
        return self._run_summary_prompt(combined_context, target_lang=target_lang, is_final_synthesis=True)

    def _run_summary_prompt(self, text: str, target_lang: str = "English", is_final_synthesis=False) -> str:
        """
        Handles the final synthesis and formatting in the target language.
        """
        instruction = f"You are a world-class educator. Respond entirely in {target_lang}."
        if is_final_synthesis:
            instruction += f" Combine these part-summaries into a cohesive study guide in {target_lang}."
        
        prompt = f"""
        {instruction}
        
        Please provide a structured study guide with headers appropriate for {target_lang}:
        1. 📌 **Executive Summary**
        2. 🔑 **Key Concepts**
        3. 📝 **Detailed Notes**
        4. 💡 **The "Big Picture"**

        Content to summarize:
        {text}
        """
        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_quiz(self, context_text: str, target_lang: str = "English") -> list:
        """
        Generates 5 questions in the specified target language.
        """
        prompt = f"""
        Act as a professor. Based on the study guide provided, create 5 challenging multiple-choice questions.
        IMPORTANT: All text (questions, options, and answers) MUST be written in {target_lang}.
        
        Return the output ONLY as a JSON array. 
        Each object must contain:
        - "question": string
        - "options": list of 4 strings
        - "answer": the exact string from the options list that is correct.

        Study Guide:
        {context_text}
        """
        
        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            raw_content = response['response']
            
            # Find the JSON array in the response
            match = re.search(r'\[\s*\{.*\}\s*\]', raw_content, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            
            return []
        except Exception as e:
            print(f"Quiz generation error: {e}")
            return []