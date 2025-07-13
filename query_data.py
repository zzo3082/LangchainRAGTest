from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# 讀取 .env 文件
load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
只回答與以下內容有關的資訊，並且不要回答與以下內容無關的問題。:

{context}

---

根據以上資訊回答問題 : {question}
"""

def main():
    quert_text= input("請輸入問題 : \n")

    # 準備 vectorDB
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search vectorDB (找出3個最相關的chunks)
    results = db.similarity_search_with_score(quert_text, k=3)
    if len(results)==0 or results[0][1]<0.7:
        print("找不到相關資料")
        return

    # 把找出來的相關chunks跟quert_text, 組到PROMPT_TEMPLATE裡面
    context_text = "\n\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context = context_text, question = quert_text)
    print(prompt)

    model = ChatOpenAI()
    #response_text = model.predict(prompt) #舊的用predict
    response_text = model.invoke(prompt) # 新的用invoke

    #sources = [doc.metadata.get("source", None) for doc, _score in results]
    #formatted_response = f"Response : {response_text.content}\nSources : {sources}"
    formatted_response = f"Response : {response_text.content}"
    print(formatted_response)

if __name__ == "__main__":
    main()