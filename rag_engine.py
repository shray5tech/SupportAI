import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferWindowMemory

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Local embedding model — runs on your machine, no API calls needed
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def load_and_chunk_documents():
    loader = DirectoryLoader(
        "./knowledge_base/",
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Loaded {len(documents)} documents → {len(chunks)} chunks")
    return chunks


def build_vectorstore(chunks):
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print("✅ Vector store created and saved")
    return vectorstore


def load_vectorstore():
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    return vectorstore


def get_chat_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )

    memory = ConversationBufferWindowMemory(
        k=5,
        memory_key="chat_history",
        return_messages=True
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=False,
        verbose=False
    )
    return chain


def initialize_bot():
    if os.path.exists("./chroma_db"):
        print("📂 Loading existing knowledge base...")
        vectorstore = load_vectorstore()
    else:
        print("🔨 Building knowledge base for first time...")
        chunks = load_and_chunk_documents()
        vectorstore = build_vectorstore(chunks)

    chain = get_chat_chain(vectorstore)
    print("🤖 SupportAI is ready!\n")
    return chain
