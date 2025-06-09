"""Debug utilities to see what google_search is doing in academic agents."""

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import your main agent
from .agent import academic_coordinator

def debug_search_with_detailed_events(query: str):
    """Comprehensive debugging to see all google_search activity."""
    
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name="academic_debug", 
        user_id="researcher1", 
        session_id="debug_session"
    )
    runner = Runner(
        agent=academic_coordinator, 
        app_name="academic_debug", 
        session_service=session_service
    )
    
    print(f"\n{'='*80}")
    print(f"🔍 DEBUGGING GOOGLE SEARCH FOR: {query}")
    print(f"{'='*80}")
    
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id="researcher1", session_id="debug_session", new_message=content)
    
    search_count = 0
    tool_calls = 0
    
    for event in events:
        agent_name = event.author or "coordinator"
        event_type = type(event).__name__
        
        print(f"\n[{agent_name.upper()}] Event: {event_type}")
        print(f"[{agent_name.upper()}] Is Final: {event.is_final_response()}")
        
        if event.content and event.content.parts:
            content_text = event.content.parts.text
            
            # Track google_search tool calls
            search_indicators = ['google_search', 'searching', 'search for', 'web search', 'query']
            if any(indicator in content_text.lower() for indicator in search_indicators):
                search_count += 1
                print(f"\n🔍 SEARCH ACTIVITY #{search_count}")
                print(f"Agent: {agent_name}")
                print(f"Search Query/Activity: {content_text}")
                print("-" * 60)
            
            # Track sub-agent delegations
            if 'academic_websearch_agent' in content_text:
                tool_calls += 1
                print(f"\n🤖 SUB-AGENT CALL #{tool_calls}")
                print(f"Delegating to: academic_websearch_agent")
                print(f"Context: {content_text[:200]}...")
                print("-" * 60)
            
            # Show academic content processing
            academic_keywords = ['paper', 'research', 'citation', 'arxiv', 'doi']
            if any(keyword in content_text.lower() for keyword in academic_keywords):
                print(f"\n📚 ACADEMIC CONTENT PROCESSING")
                print(f"Content: {content_text[:300]}...")
                print("-" * 60)
        
        if event.is_final_response():
            print(f"\n{'='*60}")
            print(f"✅ FINAL RESPONSE FROM {agent_name.upper()}")
            print(f"{'='*60}")
            if event.content and event.content.parts:
                final_text = event.content.parts.text
                print(final_text)
            break
    
    print(f"\n{'='*80}")
    print(f"📊 DEBUGGING SUMMARY")
    print(f"{'='*80}")
    print(f"Total search activities detected: {search_count}")
    print(f"Total sub-agent calls: {tool_calls}")
    print(f"Main agent: academic_coordinator")
    print(f"Sub-agents involved: academic_websearch_agent")

if __name__ == "__main__":
    # Test with academic queries
    test_queries = [
        "Find recent papers that cite the BERT paper",
        "What are the latest developments in transformer architecture?",
        "Suggest new research directions based on attention mechanisms"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'#'*100}")
        print(f"TEST {i}/{len(test_queries)}")
        print(f"{'#'*100}")
        debug_search_with_detailed_events(query)
        
        if i < len(test_queries):
            input("\nPress Enter to continue to next test...")
