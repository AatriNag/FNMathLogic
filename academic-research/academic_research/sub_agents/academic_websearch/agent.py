# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Academic_websearch_agent for finding research papers using search tools."""

import logging
import os

# Set ADK debug level
os.environ['ADK_LOG_LEVEL'] = 'DEBUG'

# Configure logging to see HTTP requests
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)

# Your existing agent code...
from google.adk import Agent
from google.adk.tools import google_search
from . import prompt
academic_websearch_agent = Agent(
    model="gemini-2.0-flash",
    name="academic_websearch_agent",
    instruction=prompt.ACADEMIC_WEBSEARCH_PROMPT,
    output_key="recent_citing_papers",
    tools=[google_search],
)
