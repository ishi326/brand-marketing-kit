BRAND MARKETING KIT 

Use Case: An AI tool that looks at a business's website and produces a marketing strategy, after targeted research and iteration, with ready to use content ideas. It is a self checking, iterative, multi step tool that allows businesses to receive ideas without worrying about the AI getting lost.

Functionality: 
 Input: You provide it with a website URL that belongs to a company/brand that you'd like recommendations for 
 Mechanics: It includes 4 AI agents, created using Gemini (but code allows for it to be OpenAI or Claude). 
    1. Research Agent: Parses the website and figures out more about the brand. What they sell, who their customers are, and what makes them different.
    2. Strategy Agent: Based on the information retrieved by the research agent, proposes one focused plan for how this business could grow sales, with reasoning behind it.
    3. Critique Agent: Critiques the strategy, looks for reasons for strategy to fail based on criterion such as feasibility, alignment with brand, evidence behind the strategy etc. It also provides feedback to the Strategy and either Approves or revises the strategy. Approved strategies move ahead to the creative agent but revised strategies must go back in an iterative loop to the strategy agent to come up with a new strategy.
    4. Creative Agent: Once the strategy passes that review, a final AI generates 5-6 specific, ready-to-shoot social media ideas that carry out the plan.
 It creates a small personalized marketing team. The iteration between Strategy and Critique remains to be the most valuable component of the model.
 Output: Brand Marketing Report with Brand Diagnosis, Recommended Strategy and Content Ideas

Use of LangChain: 
    LangChain
    The structured "forms" the AI has to fill out are built with Pydantic, a standard Python data-validation library. Using its method, .withstructuredoutput(), it takes a Pydantic model and forces AI's response to match it exactly. This helps the Critique AI agent give a verdict as to whether the Strategy aligns with the brand. The creative agent's content ideas come back as actionable items, instead of a paragraph that has to be parsed. LangChain's prompt templates and model-provider abstraction are also used throughout.
    LangGraphs
    This project is a workflow where the Critique step can send work back to the Strategy step to be redone, possibly more than once, before moving forward. LangGraph loops through workflow `graph.py` wires the four agents into a `StateGraph`, with a conditional edge that routes back to Strategy on REVISE (up to a configurable `max_revisions` cap) or forward to Creative on APPROVE (given by Critique agent).

Setup: 
 Google Gemini API key/ OpenAI key/ Anthropic Key
 1.Open a terminal in this project folder.
 2.Create a virtual environment using commands:

   python3 -m venv venv
   source venv/bin/activate       # Mac/Linux
   venv\Scripts\activate #Windows

 3.Install dependencies:

   pip install -r requirements.txt

 4.Copy `.env.example` to `.env` and add your Gemini key:

How to Run: 

    Run the following command:

    python main.py --brand-url https://www.apple.com (you can replace apple.com with any website of your choice)
    python main.py --brand-url https://example.com --output report.txt (optional, to save the report)

    The first run may take a minute or two — it makes several sequential AI calls, including any revision rounds.

Design Decisions and Trade Offs:

    1. Instagram Analysis: Nowadays, social media is a prominent marketing storefront. Being able to take a company's instagram url and scrape it would give insightful data on their marketing strategies and methods. While the url can be incorporated, Instagram scraping anonymously is extremely difficult due to security reasons. This is something that can be explored in the future as marketing quite essentially moves to social media. 
    2. Competitor Research: Researching competitiors is currently done via a free web search (no API key) rather than scraping their social accounts, and gathering information on competitors. This is a great space for evolution since it would help in performance marketing.
    3. No human in the loop: Currently, the largest drawback of this model is the potential over reliance on AI. Two AI agents are in an iterative feedback and resolution loop. In order for one AI agent to not overpower the other, or hallucinations or preserving autonomy while making decisions, a human should be added to the loop occasionally to check whether revisions are going as intended. This can be also explored in future work. 
    4. Limitations of free API keys: For this project, I used the free version of the Gemini 3.5 Flash API key, however, it is on a credit basis that expires pretty quickly since each execution makes about 4-8 API calls. After a few tests, I had to switch to a lower level "lite" model which changed the Critique Agent's apparent behavior since this agent in particular requires strong thinking skills. If I had more time and resources, I would try to make the Critique agent more robust since it's a valuable asset to this model. 
    5. LLM is swappable: The system was built and tested against Gemini, but Anthropic and OpenAI branches are already wired in and would work with a valid key and no code changes elsewhere. This matters practically because different clients often have different LLMs. 

Hierarchy
    - src (source folder)
        - ingestion 
            - brand_scraper.py (scrapes the website to get data about the brand and do initial research)
        - agents.py (contains all the 4 AI agents, their prompts and responses)
        - config.py (allows to change LLMs)
        - graph.py (flowchart and loop process for entire model)
        - output.py (report format (final))
        - schemas.py (creates pydantic tables that guide AI responses by the agents in a particular format)
        - state.py (shared datastructure between all agents)

    - .env.example (example of env file, make a copy and fill with your API to continue)
    - main.py (file to be executed by user)
    - README.md (this file - instructions to operate and understand)
    - requirements.txt (contains all packages that need to be installed to run this model)