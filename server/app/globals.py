# TODO: fix the chroamaDB hot re-init problem later
from typing import Optional
from .kb.query_chroma import Query

# This dictionary will act as a container for our global objects
app_globals = {}

def get_query_agent() -> Optional[Query]:
    """
    A dependency injection function to get the Query Agent instance anywhere in the app.
    """
    return app_globals.get("chroma_query_agent")
