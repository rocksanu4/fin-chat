import os
from langchain.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


# 1. Get a retriever based on user access
def get_retriever_for_user(user, persist_path="./chroma_store"):
    # You can pass OpenAI embedding here (does NOT use API per query)
    embedding_fn = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")  # Or replace with st.secrets
    )

    vectorstore = Chroma(
        persist_directory=persist_path,
        embedding_function=embedding_fn
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 5,
            "filter": {
                "company": {"$in": user["companies"]}
            }
        }
    )


# 2. Create the chat chain with a strong prompt
def get_chat_chain(retriever):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",  # Or "gpt-4"
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")  # Or use st.secrets["OPENAI_API_KEY"]
    )

    prompt_template = PromptTemplate.from_template("""
You are a financial analyst assistant. Answer the user's question using only the provided financial context.

- Use exact numbers and currency (₹, crore, etc.) as they appear.
- If the question is about performance, summarize revenue, income, margins, and growth.
- If the data is not in context, say so — don't make up answers.

Context:
{context}

Question:
{question}
""")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,  # Toggle True/False depending on use
        chain_type_kwargs={"prompt": prompt_template}
    )

    return qa_chain
