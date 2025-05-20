from langchain_tavily import TavilySearch
from davia import Davia
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from classes import PersonInfo, CardTitle, Card, StartupIdea, MatchResult
from typing import List
import asyncio

load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
)


def get_person_info(
    name_person: str,
):
    tool = TavilySearch(
        max_results=10,
        topic="general",
        include_answer=True,
        include_raw_content=True,
        include_images=False,
        include_image_descriptions=True,
        # search_depth="basic",
        # time_range="day",
        include_domains=["https://www.linkedin.com/"],
        # exclude_domains=None
    )

    info_about_person = tool.invoke(
        {"query": f"{name_person} information"},
        stream=False,
    )

    response = model.with_structured_output(PersonInfo).invoke(
        [
            SystemMessage(
                content="""Given the information about a person, extract key professional signals and insights, including:
	•	Current role & company
    •	Location
	•	Past roles & career progression
	•	Education
	•	Skills & endorsements
	•	Industries involved
	•	Notable keywords or patterns (e.g. founder, product, AI, etc.)
	•	Any potential flags (e.g. frequent job changes)

Output should be structured, give as much detailed as possible, and be ready to compare with another profile. Your response should be in english.
                """
            ),
            HumanMessage(
                content=f"Here is the information I found on the internet about {name_person}: {info_about_person}"
            ),
        ],
    )
    return response


# Async wrappers for parallel execution
async def get_person_info_async(name_person: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_person_info, name_person)


def create_card_content(profile1: PersonInfo, profile2: PersonInfo, card_title: str):
    class CardContent(BaseModel):
        score: int
        insight: str

    card_content = model.with_structured_output(CardContent).invoke(
        [
            SystemMessage(
                content=f""" You're building a fun, addictive co-founder matchmaking app.

Given the two profiles below, generate a playful, witty, and truly unique comparison card titled {card_title}.

The card must include:
	•	A score from 0 to 100 (how well they match on that specific dimension)
	•	A short, funny insight (like something you'd see on a dating app, but professional). Do not mention the score in the insight. 

IMPORTANT: Multiple cards for different card titles are generated in parallel. You must ensure that each card is uniquely and specifically adapted to its own card title and dimension. 

Keep it light, human, and clever — but still grounded in the data.

Write in English. Avoid dry or formal tones — aim for addictive and scroll-worthy.    """
            ),
            HumanMessage(
                content=f"Here are the profiles to compare: {profile1} and {profile2}"
            ),
        ],
    )

    return card_content


# Async wrappers for parallel execution
async def create_card_content_async(profile1, profile2, card_title):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, create_card_content, profile1, profile2, card_title
    )


def find_startup_ideas(profile1: str, profile2: str):
    class Ideas(BaseModel):
        ideas: List[StartupIdea]

    startup_idea = model.with_structured_output(Ideas).invoke(
        [
            SystemMessage(
                content="You are the genius friend who always has wild startup ideas. \
                    Given the two profiles below, come up with three startup ideas they could build together \
                        — make them sound cool, original, and just the right amount of crazy. For each idea, \
                            add a really short why this works explanation based on their backgrounds. \
                                Keep the idea really short, like 10 words max. The reason could be more developed (100 words max)."
            ),
            HumanMessage(
                content=f"Here are the profiles to compare: {profile1} and {profile2}"
            ),
        ],
    )
    return startup_idea


app = Davia()


@app.task
async def find_match_result(name_person1: str, name_person2: str) -> MatchResult:
    """
    Find the match result for two people :
    - Get the person info (in parallel)
    - Create cards for each CardTitle (in parallel)
    - Calculate overall match score (average, invert conflict probability)
    - Get startup ideas
    - Build and return MatchResult

    Args :
        name_person1 : str
        name_person2 : str

    Returns :
        MatchResult
    """
    # Fetch both profiles in parallel
    profile1, profile2 = await asyncio.gather(
        get_person_info_async(name_person1), get_person_info_async(name_person2)
    )

    # Generate all cards in parallel
    card_titles = list(CardTitle)
    card_contents = await asyncio.gather(
        *[
            create_card_content_async(profile1, profile2, card_title.value)
            for card_title in card_titles
        ]
    )
    card_map = {
        card_title: Card(
            title=card_title, score=card_content.score, insight=card_content.insight
        )
        for card_title, card_content in zip(card_titles, card_contents)
    }

    # Calculate overall match score (average, invert conflict probability)
    scores = [
        card_map[CardTitle.SKILL_COMPLEMENTARITY].score,
        card_map[CardTitle.INDUSTRY_EXPERIENCE_ALIGNMENT].score,
        100 - card_map[CardTitle.CONFLICT_PROBABILITY].score,  # invert
        card_map[CardTitle.GROWTH_CATALYST_POTENTIAL].score,
        card_map[CardTitle.CULTURAL_FIT_INDEX].score,
        card_map[CardTitle.CRITIQUE_OPENNESS].score,
    ]
    overall_match_score = int(sum(scores) / len(scores))

    # Get startup ideas (can be made async if needed)
    startup_ideas_obj = await asyncio.get_event_loop().run_in_executor(
        None, find_startup_ideas, profile1, profile2
    )
    startup_ideas = (
        startup_ideas_obj.ideas if hasattr(startup_ideas_obj, "ideas") else []
    )

    # Build and return MatchResult
    match_result = MatchResult(
        overall_match_score=overall_match_score,
        skill_complementarity=card_map[CardTitle.SKILL_COMPLEMENTARITY],
        industry_experience_alignment=card_map[CardTitle.INDUSTRY_EXPERIENCE_ALIGNMENT],
        conflict_probability=card_map[CardTitle.CONFLICT_PROBABILITY],
        growth_catalyst_potential=card_map[CardTitle.GROWTH_CATALYST_POTENTIAL],
        cultural_fit_index=card_map[CardTitle.CULTURAL_FIT_INDEX],
        critique_openness=card_map[CardTitle.CRITIQUE_OPENNESS],
        startup_ideas=startup_ideas,
    )
    return match_result


if __name__ == "__main__":
    app.run()
