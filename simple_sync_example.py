"""
Module with examples for synchronous functions.
"""
import logging
import uuid
from yajaw import jira, ApiType
from observability.logs import setup_logging, context_id

# Set up logging and get Logger
setup_logging()
logger = logging.getLogger("example")

def use_fetch_all_projects() -> list[dict]:
    context_id.set(uuid.uuid4())
    logger.info("Starting to fetch all projects...")
    projs = jira.fetch_all_projects()
    logger.info("Completed fetching all projects...")

def use_fetch_project() -> dict:
    context_id.set(uuid.uuid4())
    logger.info("Starting to fetch a single project...")
    proj = jira.fetch_project(project_key="EMI")
    logger.info("Completed fetching a single project...")

def use_fetch_projects_from_list() -> list[dict]:
    context_id.set(uuid.uuid4())
    logger.info("Starting to fetch a project list...")
    projs = jira.fetch_projects_from_list(project_keys=["EMI", "ETOE"])
    logger.info("Completed fetching a project list...")

def use_fetch_issue() -> dict:
    context_id.set(uuid.uuid4())
    logger.info("Starting to fetch a single issue...")
    issue = jira.fetch_issue(issue_key="ABC-1", api=ApiType.CLASSIC)
    issue = jira.fetch_issue(issue_key="ABC-1", api=ApiType.AGILE)
    logger.info("Completed fetching a single issue...")

def use_search_issues() -> list[dict]:
    context_id.set(uuid.uuid4())
    logger.info("Starting to search for issues...")
    issues = jira.search_issues(jql="project in (EMI)")
    logger.info("Completed searching for issues...")


if __name__ == "__main__":

    use_fetch_all_projects()
    use_fetch_project
    use_fetch_projects_from_list
    use_fetch_issue()
    use_search_issues()