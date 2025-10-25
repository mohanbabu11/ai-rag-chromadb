
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
import os
from typing import List

print ("Knowledge Case Module")

class KnowledgeCase:
    def __init__(self, 
                 api_key: str, 
                 persist_directory: str="./data/chroma_db", 
                 collection_name: str="knowledge_case" ):
        print ("Initializing Knowledge Case")
        print("api_key:", api_key)
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

        self.vectorstore = Chroma(collection_name=collection_name,
                                  embedding_function=self.embeddings,
                                  persist_directory=persist_directory)
        

        #self.vectorstore = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)

    def add_documents(self, documents: List[Document]) -> None:
        print ("Adding documents to vectorstore")
        self.vectorstore.add_documents(documents)

    def add_texts(self, texts: List[str], metadatas: List[dict] = None) -> None:
        print ("Adding texts to vectorstore")
        self.vectorstore.add_texts(texts, metadatas=metadatas)

    def query(self, query_text: str, k: int = 5) -> List[Document]:
        return self.vectorstore.similarity_search(query_text, k=k)
    
    def similarity_search(self, query_text: str, k: int = 3) -> List[Document]:
        return self.vectorstore.similarity_search(query_text, k=k)

    def similarity_search_with_score(self, query_text: str, k: int = 3) -> List[tuple]:
        return self.vectorstore.similarity_search_with_score(query_text, k=k)
    
    @staticmethod
    def create_sample_knowledge_base(api_key: str) -> "KnowledgeCase":
        print ("api key in create_sample_knowledge_base:", api_key)

        kc = KnowledgeCase(api_key=api_key)

        sample_documents = [
            Document(
                page_content="Our return policy allows customers to return items within 30 days of purchase for a full refund. Items must be unused and in original packaging. To initiate a return, log into your account and select 'Return Items' from your order history.",
                metadata={"source": "returns_policy.txt"}
            ),
            Document(
                page_content="We offer three shipping options: Standard shipping (5-7 business days, $5.99), Express shipping (2-3 business days, $12.99), and Overnight shipping (1 business day, $24.99). Free standard shipping is available on orders over $50.",
                metadata={"source": "shipping_info.txt"}
            ),
            Document(
                page_content="To track your order, visit our website and click 'Track Order' in the top menu. Enter your order number and email address. You will also receive tracking information via email once your order ships.",
                metadata={"source": "order_tracking.txt"}
            ),
            Document(
                page_content="We accept the following payment methods: Visa, Mastercard, American Express, Discover, PayPal, Apple Pay, and Google Pay. We do not accept other form of payments.All transactions are secured with 256-bit SSL encryption.",
                metadata={"source": "payment_methods.txt"}
            ),
            Document(
                page_content="Our customer support team is available Monday through Friday from 9:00 AM to 6:00 PM EST. Weekend support is available Saturday from 10:00 AM to 4:00 PM EST. We are closed on Sundays and major holidays.",
                metadata={"source": "contact_hours.txt"}
            ),
            Document(
                page_content="Refunds are processed within 5-7 business days after we receive your returned item. The refund will be credited to your original payment method. Please note that shipping costs are non-refundable unless the return is due to our error.",
                metadata={"source": "returns_policy.txt"}
            ),
            Document(
                page_content="For expedited order processing, place your order before 2:00 PM EST on business days. Orders placed after this time will be processed the next business day. International shipping typically takes 7-14 business days depending on the destination.",
                metadata={"source": "shipping_info.txt"}
            ),
            Document(
                page_content="You can contact our customer support team via email at support@example.com, by phone at 1-800-555-0123, or through our live chat feature available on our website during business hours.",
                metadata={"source": "contact_hours.txt"}
            )
        ]

        kc.add_documents(sample_documents)
        return kc
    