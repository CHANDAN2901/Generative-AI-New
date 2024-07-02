import streamlit as st
import warnings
from crewai import Agent, Task, Crew
from langchain_community.llms import HuggingFaceHub
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Warning control
warnings.filterwarnings('ignore')

# Streamlit app
st.title("AI Content Generator")

# User input
topic = st.text_input("Enter the topic for content generation:", "Artificial Intelligence")

if st.button("Generate Content"):
    with st.spinner("Generating content... This may take a few minutes."):
        # Initialize LLM
        llm = HuggingFaceHub(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_KEY'),
            task="text-generation",
        )

        # Agent definitions
        planner = Agent(
            role="Content Planner",
            goal=f"Plan engaging and factually accurate content on {topic}",
            backstory=f"You're working on planning a blog article about the topic: {topic}. "
                      "You collect information that helps the audience learn something "
                      "and make informed decisions. Your work is the basis for "
                      "the Content Writer to write an article on this topic.",
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

        writer = Agent(
            role="Content Writer",
            goal=f"Write insightful and factually accurate opinion piece about the topic: {topic}",
            backstory=f"You're working on writing a new opinion piece about the topic: {topic}. "
                      "You base your writing on the work of the Content Planner, who provides an outline "
                      "and relevant context about the topic. You follow the main objectives and "
                      "direction of the outline, as provide by the Content Planner. "
                      "You also provide objective and impartial insights and back them up with information "
                      "provide by the Content Planner. You acknowledge in your opinion piece "
                      "when your statements are opinions as opposed to objective statements.",
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

        editor = Agent(
            role="Editor",
            goal="Edit a given blog post to align with the writing style of the organization.",
            backstory="You are an editor who receives a blog post from the Content Writer. "
                      "Your goal is to review the blog post to ensure that it follows journalistic best practices, "
                      "provides balanced viewpoints when providing opinions or assertions, "
                      "and also avoids major controversial topics or opinions when possible.",
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

        # Task definitions
        plan = Task(
            description=(
                f"1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
                "2. Identify the target audience, considering their interests and pain points.\n"
                "3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
                "4. Include SEO keywords and relevant data or sources."
            ),
            expected_output="A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.",
            agent=planner,
        )

        write = Task(
            description=(
                f"1. Use the content plan to craft a compelling blog post on {topic}.\n"
                "2. Incorporate SEO keywords naturally.\n"
                "3. Sections/Subtitles are properly named in an engaging manner.\n"
                "4. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
                "5. Proofread for grammatical errors and alignment with the brand's voice.\n"
            ),
            expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
            agent=writer,
        )

        edit = Task(
            description="Proofread the given blog post for grammatical errors and alignment with the brand's voice.",
            expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
            agent=editor
        )

        # Create and run the crew
        crew = Crew(
            agents=[planner, writer, editor],
            tasks=[plan, write, edit],
            verbose=2
        )

        result = crew.kickoff(inputs={"topic": topic})

        # Display the result
        st.markdown(result)

st.info("Note: This application uses an API key stored in an environment variable. Ensure you have set up your .env file correctly.")