INSTRUCTIONS = '''
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
'''

PROMPT_TEMPLATE = '''
QUESTION: {question}

CONTEXT:
{context}
'''.strip()


class RAGBase:

    def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        filename ='llm-zoomcamp',
        model='openai/gpt-oss-120b'
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.filename  = filename
        self.prompt_template = prompt_template
        self.model = model

    def search(self, query, num_results=5):
        boost_dict = {'content': 3.0}
        #filter_dict = {'filename': self.filename }

        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            #filter_dict=filter_dict
        )

    def build_context(self, search_results):
        lines = []

        for doc in search_results:
            lines.append('Q: ' + doc['filename'])
            lines.append('A: ' + doc['content'])
            lines.append('')

        return '\n'.join(lines).strip()

    def build_prompt(self, query, search_results):
        context = self.build_context(search_results)
        return self.prompt_template.format(
            question=query, context=context
        )

    def llm(self, prompt):
        input_messages = [
            {'role': 'system', 'content': self.instructions},
            {'role': 'user', 'content': prompt}
        ]

        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=input_messages
        )

        # RETURN THE ENTIRE RESPONSE OBJECT
        return response

    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        
        # Get the full response object from the LLM
        response = self.llm(prompt)
        
        # Extract the answer text
        answer = response.choices[0].message.content
        
        # Extract the usage metadata (contains prompt_tokens, completion_tokens, etc.)
        usage = response.usage
        
        # Return as a tuple
        return answer, usage