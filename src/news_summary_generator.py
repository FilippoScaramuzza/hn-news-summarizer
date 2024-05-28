from huggingface_hub import InferenceClient
import json

class NewsSummaryGenerator:
    def __init__(self, model_name, api_token):
        self.client = InferenceClient(model=model_name, token=api_token)

    def generate_summary(self, html_content):
        content = html_content[:32768]
        # if len(content) < 1000:
        #     for _ in range(1000 // len(content) + 2):
        #         content += content

        input_prompt = f'''
        <s>[INST] You are a helpful news summarizer assistant. Your task is to generate a valid JSON object based on the summary of the given news. 
        The fields must be just: topic, key_points (add relevant emojis to enhance the readibility) and reading_time.
        Your ouput must be just the JSON object, so starting with a {{ and ending with a }}. Don't write anything but just the produced JSON object.
        So for instance the following:

 ICQ Sign In Eng Eng Rus ICQ will stop working from June 26 You can chat with friends in VK Messenger, and with colleagues in VK WorkSpace

would be converted to:[/INST]
{{
  "topic": "ICQ Discontinuation Announcement",
  "key_points": [
    "⏰ ICQ will cease operations on June 26.",
    "💬 Users are encouraged to migrate to VK Messenger for personal chats.",
    "👔 VK WorkSpace is recommended for professional communication."
  ],
  "reading_time": "1 minute"
}}
</s>
[INST]
{content}
[/INST]

        {content}
        ''' 
        
        response = self.client.text_generation(
            input_prompt,
            max_new_tokens=2000
        )

        return json.loads(response)

# Example usage:
# generator = NewsSummaryGenerator(model_name="mistralai/Mistral-7B-Instruct-v0.2", api_token="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")
# summary = generator.generate_summary(html_content)
