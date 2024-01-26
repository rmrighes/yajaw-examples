"""
Module with examples for synchronous functions.
"""
import logging
import uuid

from yajaw import context_id, jira

from observability.logs import setup_logging

setup_logging()

# Get the custom logger
logger = logging.getLogger("example")
logger.setLevel(logging.INFO)

context_id.set(uuid.uuid4())
logger.info("Starting to fetch all projects...")
projs = jira.fetch_all_projects()
logger.info("Completed fetching all projects...")
for proj in projs:
    logger.info(f"Return from {__name__}: {proj['key']} -- {proj['name']}")

for _ in range(10):
    context_id.set(uuid.uuid4())
    logger.info("Starting to fetch all projects...")
    projs = jira.fetch_all_projects()
    logger.info("Completed fetching all projects...")

context_id.set(uuid.uuid4())
logger.info("Starting to fetch a project...")
proj = jira.fetch_project(project_key="ABC")
logger.info("Completed fetching a project...")
logger.info(f"Return from {__name__}: {proj['key']} -- {proj['name']}")

context_id.set(uuid.uuid4())
logger.info("Starting to search for issues...")
projs = jira.search_issues(jql="project in (ABC)")
logger.info("Completed searching for issues...")
