from langchain.llms import GooglePalm
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
from few_shot import examples
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from dotenv import load_dotenv
load_dotenv()
import os

def analysis_chain():
    db = SQLDatabase.from_uri(f"postgresql://{os.environ['db_user']}:{os.environ['db_password']}@{os.environ['db_host']}:5432/{os.environ['db_name']}")
    llm = GooglePalm(temperature=0.1)

    example_prompt = PromptTemplate(
        input_variables=['Question','SQLQuery','SQLResult',"Answer"],
        template= "\nQuestion:{Question}\nSQLQuery:{SQLQuery}\nSQLResult:{SQLResult}\nAnswer:{Answer}"
    )

    embeddings = HuggingFaceEmbeddings()

    to_vectorize = [' '.join(example.values()) for example in examples]

    vectorstore = FAISS.from_texts(to_vectorize, embeddings, metadatas = examples)

    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore,k=2)

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=_mysql_prompt,
        suffix=PROMPT_SUFFIX, 
        input_variables=['Question','SQLQuery','SQLResult',"Answer"],
    )

    local_chain = SQLDatabaseChain.from_llm(llm,db,prompt=few_shot_prompt,verbose = True)

    return local_chain

