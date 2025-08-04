from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from login import Login 

class Split:
    #chunking text using langchain library
    def chunk_text_with_langchain(self, text: str, chunk_size=500, chunk_overlap=300):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        return splitter.create_documents([text])


    #create documents and optionally add metadata
    def _create_document_to_store(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        document = self.chunk_text_with_langchain(raw_text)
        for doc in document:
            doc.metadata["source"] = "reliance_ar2024"
            doc.metadata["company"] = "Reliance"

        return document
        

    # embedding and vectorizing into vectordb chroma
    def embed_and_vectorize(self, document):
        embedding = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
        return Chroma.from_documents(
            documents=document,
            embedding=embedding,
            persist_directory="./chroma_ollama"
        )


    def vector_retriever(self, user, vectorStore: Chroma):
        return vectorStore.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 5,
                "filter": {
                    "company": {"$in": user["companies"]}
                }
            }
        )

vector = Split()
document = vector._create_document_to_store(path="C:/Users/rocks/Developer/fin_chat/reliance_raw_text.txt") # type: ignore

vectorstore = vector.embed_and_vectorize(document= document)

user = Login().login(username="ambani")
vector.vector_retriever(user=user, vectorStore=vectorstore)
