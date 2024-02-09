import os
import sys
backend_folder = f"{os.getcwd()}/backend"
sys.path.append(backend_folder)
from embedding.rag_wrapper import RagWrapper


def main():
    try:


        # rag
        repo_url = "https://github.com/esphome/esphome"
        branch = "dev"
        file_type = ".py"
        ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)

        


        choice = input("Choose HuggingFacePipeline ('h') or OpenLLM ('o'): ").lower().strip()
        if choice == 'h':

            from llm.llm_model import LlmModel

            from langchain_wrapper.lang_wrapper import LangWrapper
            from llm.model_names import code_llama_model_13b_instruct

            # model
            model_name = code_llama_model_13b_instruct
            model = LlmModel(model_name=model_name)



            # langchain
            langchain_wrapper = LangWrapper(model=model)
            langchain_wrapper.add_rag_wrapper(ragWrapper)
            langchain_wrapper.setup_rag_llm_chain()

            question = """
                Briefly tell me what the codegen.py file does
                """
            generated_text = langchain_wrapper.invoke_llm_chain(question)
            history = generated_text["chat_history"]  # type: ignore
            # gen_text = model.generate_text(question)
            print(generated_text["answer"])  # type: ignore

            question = """
                output EXATCLY the COMPLETE code of 'iter_components' function AS IS
                """
            generated_text = langchain_wrapper.invoke_llm_chain(question=question)

            # gen_text = model.generate_text(question)
            print(generated_text["answer"])  # type: ignore

            question = """
                what is the path of a02yyuw.cpp file in the repository ?
                """
            generated_text = langchain_wrapper.invoke_llm_chain(question=question)

            # gen_text = model.generate_text(question)
            print(generated_text["answer"])  # type: ignore

            langchain_wrapper.cleanup()




            
        elif choice == 'o':

            print("OpenLLM")


            from langchain_community.llms import OpenLLM
            from langchain.prompts import PromptTemplate
            from langchain.chains.question_answering import load_qa_chain
            from langchain_community.llms import OpenLLM


            server_url = "http://localhost:3000"
            llm = OpenLLM(server_url=server_url)


            # Prompt
            template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer. 
            Keep the answer as concise as possible. 
            {context}
            Question: {question}
            Helpful Answer:"""
            QA_CHAIN_PROMPT = PromptTemplate(
                input_variables=["context", "question"],
                template=template,
            )

            # Docs
            question = "Write a unit test for the gpio_base_schema method, based on the specification of gpio_base_schema."
            docs = ragWrapper.retriever.get_relevant_documents(question)

            # Chain
            chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)
            output = chain.invoke({"input_documents": docs, "question": question}, return_only_outputs=True)
            print(output['output_text'])







        else:
            print("Invalid choice. Exiting.")
            return
            

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
