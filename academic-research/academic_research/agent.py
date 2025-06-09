
import logging
import sys
import urllib3

# Enable HTTP request logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

# Enable urllib3 debug logging to see all HTTP requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
logging.getLogger("requests.packages.urllib3").setLevel(logging.DEBUG)

# Enable httpx logging (used by newer versions)
logging.getLogger("httpx").setLevel(logging.DEBUG)
logging.getLogger("httpcore").setLevel(logging.DEBUG)

# Create specific logger for search tool requests
search_request_logger = logging.getLogger('google_search_requests')
search_request_logger.setLevel(logging.DEBUG)

# Format to clearly show HTTP requests
formatter = logging.Formatter('🌐 HTTP: %(asctime)s - %(name)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
search_request_logger.addHandler(handler)

# Your existing agent code...
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from . import prompt
from .sub_agents.academic_newresearch import academic_newresearch_agent
from .sub_agents.academic_websearch import academic_websearch_agent

MODEL = "gemini-2.0-flash"

# Add a logger for your agent
logger = logging.getLogger('academic_coordinator')

academic_coordinator = LlmAgent(
    name="academic_coordinator",
    model=MODEL,
    description=(
        "analyzing seminal papers provided by the users, "
        "providing research advice, locating current papers "
        "relevant to the seminal paper, generating suggestions "
        "for new research directions, and accessing web resources "
        "to acquire knowledge"
    ),
    instruction=prompt.ACADEMIC_COORDINATOR_PROMPT,
    output_key="seminal_paper",
    tools=[
        AgentTool(agent=academic_websearch_agent),
        AgentTool(agent=academic_newresearch_agent),
    ],
)

root_agent = academic_coordinator

# Log when agent is initialized
logger.info("Academic coordinator agent initialized with web search capabilities")
