from pydantic import BaseModel, Field


class RankedItem(BaseModel):
    """One recommended item.

    The descriptions are what the model reads under structured output, so the
    per-field guidance the old prompt spelled out in its JSON block lives here.
    """

    id: int = Field(
        description="The candidate's id, copied exactly from the candidate list"
    )
    title: str = Field(
        description="The candidate's title, copied from the candidate"
    )
    description: str = Field(
        description="One or two lines on what this video covers"
    )
    difficulty: str = Field(
        description="The difficulty level of this item"
    )
    why_relevant: str = Field(
        description="One or two sentences on why this item is relevant to this "
                    "specific student, referencing their topics, gaps and goals"
    )


class RankedRecommendations(BaseModel):
    summary: str = Field(
        description="One sentence describing the personalised learning strategy "
                    "behind this ranking"
    )
    ranked: list[RankedItem] = Field(
        default_factory=list,
        description="The recommended items, best first",
    )
