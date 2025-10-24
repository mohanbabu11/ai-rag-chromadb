#connect to model and create graph. 
# handles customer query and returns the answer
from tkinter import END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from knowledge_case import KnowledgeCase

print ("Graph Module")

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    query :str
    retrieved_context: str
    needs_knowledge: bool
    response: str
    session_id: str

class CustomerCareAgentGraph:
    def __init__(self, api_key: str, model: str="gemini-2.5-flash"):

        self.api_key = api_key

        self.llm = ChatGoogleGenerativeAI(model=model, 
                                          api_key=api_key, 
                                          temparature=0.2, 
                                          max_output_tokens=1024)


        self.chat_model = ChatGoogleGenerativeAI(model="models/chat-bison-001", api_key=api_key)

        self.knowledge_case = KnowledgeCase.create_sample_knowledge_base(api_key=api_key)
        self.graph = self._build_graph()

        self.graph.add_state(
            name="customer_care_agent",
            model=self.chat_model,
            prompt=self.prompt_template,
            input_keys=["retrieved_context", "query"],
            output_key="response"
        )

    def should_retrieve_knowledge(self, state: AgentState) -> bool:
        return "retrieve" if state['needs_knowledge'] else "generate"


    def _classify_need_for_knowledge(self, state: AgentState) -> None:
        classifier_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a query classifier. Determine if the customer query requires
            looking up company policies, product information, or specific facts.

            Answer with ONLY 'YES' or 'NO'.

            Answer YES if the query is about:
            - Return policies, shipping, warranties
            - Product details, pricing, availability
            - Company policies or procedures
            - Order tracking or status

            Answer NO if the query is:
            - A general greeting or thank you
            - A simple question that doesn't need specific facts
            - An emotional expression"""),
            ("human", "{query}")
        ])


        chain = classifier_prompt | self.llm
        response = chain.invoke({"query": state["query"]})
        needs_kb = "YES" in response.content.upper()

        return {
            **state,
            "needs_knowledge": needs_kb,
            "messages": state["messages"] + [AIMessage(content=f"[Classification: {'Needs KB' if needs_kb else 'No KB needed'}]")]
        }

    def _retrieve_knowledge(self, state: AgentState) -> AgentState:
        
        if not state["needs_knowledge"]:
            return {**state, "retrieved_context": ""}

        results = self.knowledge_case.similarity_search(state['query'], k=3)
        context = "\n\n".join([doc.page_content for doc in results])

        return {
            **state,
            "retrieved_context": context,
            "messages": state["messages"] + [AIMessage(content=f"[Retrieved {len(results)} documents from knowledge base]")]
        }
    
    def _generate_response(self, state: AgentState) -> AgentState:
        if state["needs_knowledge"] and state["retrieved_context"]:
            prompt = f"""Using the following retrieved context from the knowledge base, answer the customer query accurately.

            Important:
            - If the context contains the answer, use it to respond.
            - If the context does NOT contain the answer, acknowledge that you don't have the information.
            - Always maintain a polite and professional tone.
            
            Context: {state["retrieved_context"]}
            Query: {state["query"]}
            """
            response = self.llm.invoke({"prompt": prompt})
            return {
                **state,
                "response": response,
                "messages": state["messages"] + [AIMessage(content="[Generated final response]")]
            }
        else:
            prompt = f"""Answer the customer query accurately and politely.

            Query: {state["query"]}
            """
            response = self.llm.invoke({"prompt": prompt})
            return {
                **state,
                "response": response,
                "messages": state["messages"] + [AIMessage(content="[Generated final response]")]
            }
        

    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(AgentState)
        workflow.add_node("classify", self._classify_need_for_knowledge)
        workflow.add_node("retrieve", self._retrieve_knowledge)
        workflow.add_edge("generate", self._generate_response)

        workflow.set_entry_point("classify")

        workflow.add_conditional_edge("classify", 
                                      self.should_retrieve_knowledge, 
                                      {
                                          "retrieve": "retrieve",
                                          "generate": "generate"
                                       })
        
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile()