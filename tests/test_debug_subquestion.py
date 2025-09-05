#!/usr/bin/env python3
"""Debug SubQuestionQueryEngine to find root cause"""

from dotenv import load_dotenv
load_dotenv()
import os

from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler, CBEventType, EventPayload
from qdrant_client import QdrantClient

# Configure settings
Settings.embed_model = OpenAIEmbedding(
    model='text-embedding-3-small',
    api_key=os.getenv('OPENAI_API_KEY'),
    api_base='https://api.openai.com/v1'
)

Settings.llm = OpenAILike(
    model='claude-3-5-sonnet-20241022',
    api_key=os.getenv('ELECTRONHUB_API_KEY'),
    api_base='https://api.electronhub.ai/v1',
    is_chat_model=True
)

# Setup debugging
llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([llama_debug])

client = QdrantClient(url='http://localhost:6333')
vector_store = QdrantVectorStore(client=client, collection_name='semantic-search-service')
index = VectorStoreIndex.from_vector_store(vector_store)

# Test direct query first
print("=" * 50)
print("TESTING DIRECT QUERY ENGINE:")
print("=" * 50)
query_engine = index.as_query_engine(similarity_top_k=10, similarity_cutoff=0.2)
direct_result = query_engine.query('What are the main functions?')
print(f"Direct result: {str(direct_result)[:200]}")
print(f"Result type: {type(direct_result)}")
print(f"Result attributes: {dir(direct_result)}")

# Now test SubQuestionQueryEngine with debugging
print("\n" + "=" * 50)
print("TESTING SUBQUESTION ENGINE WITH DEBUG:")
print("=" * 50)

tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name='semantic-search',
        description='Search semantic-search-service codebase'
    )
)

try:
    # Create engine with callbacks
    engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=[tool],
        callback_manager=callback_manager,
        verbose=True
    )
    
    result = engine.query('What are the main functions and how do they work?')
    
    print(f"\nFinal result: {result}")
    print(f"Result type: {type(result)}")
    
    # Debug the sub-question events
    print("\n" + "=" * 50)
    print("SUB-QUESTION DEBUG INFO:")
    print("=" * 50)
    
    for i, (start_event, end_event) in enumerate(
        llama_debug.get_event_pairs(CBEventType.SUB_QUESTION)
    ):
        if end_event and hasattr(end_event, 'payload'):
            qa_pair = end_event.payload.get(EventPayload.SUB_QUESTION)
            if qa_pair:
                print(f"\nSub Question {i}:")
                print(f"  Q: {qa_pair.sub_q.sub_question.strip() if hasattr(qa_pair, 'sub_q') else 'N/A'}")
                print(f"  A: {qa_pair.answer.strip() if hasattr(qa_pair, 'answer') else 'N/A'}")
                print(f"  Answer type: {type(qa_pair.answer) if hasattr(qa_pair, 'answer') else 'N/A'}")
    
    # Check LLM events
    print("\n" + "=" * 50)
    print("LLM EVENTS:")
    print("=" * 50)
    
    llm_events = llama_debug.get_llm_inputs_outputs()
    for i, (input_str, output_str) in enumerate(llm_events):
        print(f"\nLLM Call {i}:")
        print(f"  Input: {input_str[:200]}...")
        print(f"  Output: {output_str[:200]}...")
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    print(traceback.format_exc())

print("\n" + "=" * 50)
print("FULL TRACE:")
print("=" * 50)
# The trace will print automatically due to print_trace_on_end=True