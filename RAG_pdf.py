from pdf_uploader import *
from embeddings_geneeator import *
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,SystemMessage
from cli import *
from markrender import MarkdownRenderer

renderer = MarkdownRenderer(stream_code=False,theme = "monokai")
llm = ChatGroq(model = "llama-3.1-8b-instant")
def main():
    choice = interface()

    if choice == "Select PDF":
        choice = PDF_selection()
        if choice == "Back":
            main()
        vectordb = load_existing_db(choice)
    elif choice == "Upload PDF":
        print("upload your pdf: ")
        path = upload_pdf()
        vectordb = embedd(path)
    else:
        return
    while True: 
        query = input("user: ") 
        if query == "exit": 
            return   
        elif query == "back":
            main()
            break
        macthed_chunks = vectordb.similarity_search(query,k=3)
        retrived_text = ""
        for i,chunk in enumerate(macthed_chunks):
            retrived_text += f"\n-----------source{i+1}----------\n{chunk.page_content}"
        chunks = retrived_text
        # chat_history.append(HumanMessage(content = query))
        messages = [
            SystemMessage(content="""
                You are a strict AI assistant.

                You must answer ONLY using the provided context.

                If the answer is not explicitly present in the context,
                respond exactly with:

                "I don't know based on the provided context."

                Do NOT use outside knowledge.
                Do NOT guess.
                """),
            HumanMessage(content = f"""
                            context :
                                    {chunks},
                        user question : 
                                        {query} 
                                        answer and mention souce number.
                            """)
        ]
        response = llm.invoke(messages)
        renderer.render(response.content)
        renderer.finalize()

if __name__ == "__main__":
    main()