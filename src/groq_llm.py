from groq import Groq
import os
from logger import logging

def model(resume_text, prompt):
    try:
        logging.info("trying to make connection with groq")

        api_key = os.getenv("groq_key")

        if not api_key:
            raise ValueError("Groq API key not found")

        client = Groq(api_key=api_key)

        logging.info("generating prompt according to use case")
        final_prompt = f"{prompt} Resume:{resume_text}"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            temperature=0
        )

        logging.info("response was successfully collected by groq")

        return response.choices[0].message.content

    except Exception as e:
        logging.error(f"error occured during communication with groq as {e}")
        raise

