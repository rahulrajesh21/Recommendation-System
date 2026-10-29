from langchain_google_genai import GoogleGenerativeAIEmbeddings


class EmbeddingService:

    def __init__(self):
       self.embedding = GoogleGenerativeAIEmbeddings(model='gemini-embedding-2')

    async def embed_text(self,text:str)->list[float]:
        return await self.embedding.aembed_query(text)

