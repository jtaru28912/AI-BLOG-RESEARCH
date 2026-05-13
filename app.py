import os
import asyncio

import streamlit as st

from dotenv import load_dotenv

from graph.workflow import app_workflow

from utils.llm import get_llm

from agents import storage_agent

# -----------------------------
# LOAD ENV
# -----------------------------

load_dotenv()

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Research Blog Assistant",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3rem;
    font-size: 18px;
    font-weight: 600;
}

.stTabs [data-baseweb="tab"] {
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------

st.title("🧠 AI Research Blog Assistant")

st.caption("""
Generate SEO + GEO optimized AI research blogs using LangGraph multi-agent workflows.
""")

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header("⚙️ Configuration")

    model_name = st.selectbox(
        "OpenAI Model",
        [
            "gpt-4o-mini",
            "gpt-4.1-mini"
        ]
    )

    temperature = st.slider(
        "Creativity",
        0.0,
        1.0,
        0.3
    )

    num_papers = st.slider(
        "Number of Papers",
        3,
        15,
        5
    )

    st.divider()

    st.markdown("""
    ### 🚀 Features

    ✅ LangGraph Workflow  
    ✅ LangChain Integration  
    ✅ Async AI Agents  
    ✅ SEO Optimization  
    ✅ GEO Optimization  
    ✅ FAQ Generation  
    ✅ ChromaDB Storage  
    """)

# -----------------------------
# OPENAI KEY
# -----------------------------

openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:

    st.error("OPENAI_API_KEY missing in .env")

    st.stop()

# -----------------------------
# LOAD LLM
# -----------------------------

llm = get_llm(
    model_name=model_name,
    temperature=temperature,
    api_key=openai_key
)

# -----------------------------
# USER INPUT
# -----------------------------

topic = st.text_input(
    "🔍 Enter Research Topic",
    placeholder="Latest advancements in Transformer Architectures"
)

# -----------------------------
# GENERATE
# -----------------------------

if st.button("🚀 Generate Blog"):

    if not topic:

        st.warning("Please enter a topic.")

        st.stop()

    async def run_workflow():

        initial_state = {

            "topic": topic,

            "num_papers": int(num_papers),

            "llm": llm,

            "papers": [],

            "extracted_data": [],

            "summaries": [],

            "insights": "",

            "blog": "",

            "seo_blog": "",

            "faq": []
        }

        result = await app_workflow.ainvoke(
            initial_state
        )

        return result

    try:

        with st.spinner(
            "Running LangGraph AI workflow..."
        ):

            result = asyncio.run(
                run_workflow()
            )

        storage_agent.store_blog(
            topic=result["topic"],
            blog=result["seo_blog"]
        )

        st.success(
            "✅ Blog Generated Successfully!"
        )

        # -----------------------------
        # TABS
        # -----------------------------

        tab1, tab2, tab3 = st.tabs([
            "📘 Blog",
            "🧠 Insights",
            "📚 Papers"
        ])

        # -----------------------------
        # BLOG
        # -----------------------------

        with tab1:

            st.markdown(
                result["seo_blog"]
            )

            st.download_button(
                label="⬇️ Download Blog",
                data=result["seo_blog"],
                file_name=f"{topic}.md",
                mime="text/markdown"
            )

            with st.expander(
                "❓ FAQ / Q&A"
            ):

                for item in result["faq"]:

                    st.markdown(
                        f"### {item['question']}"
                    )

                    st.write(
                        item["answer"]
                    )

        # -----------------------------
        # INSIGHTS
        # -----------------------------

        with tab2:

            st.markdown(
                result["insights"]
            )

        # -----------------------------
        # PAPERS
        # -----------------------------

        with tab3:

            for paper in result["papers"]:

                st.markdown(f"""
                ### {paper['title']}

                **Authors:** {", ".join(paper['authors'])}

                **Published:** {paper['published']}

                🔗 {paper['link']}
                """)

    except Exception as e:

        st.error(f"Error: {str(e)}")