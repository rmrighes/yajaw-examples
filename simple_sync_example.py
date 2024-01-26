"""
Module with examples for synchronous functions.
"""
import logging

from observability.logs import setup_logging

from yajaw import YajawConfig, jira


setup_logging()

# Get the custom logger
logger = logging.getLogger("yajaw")
logger.setLevel(logging.INFO)

projs = jira.fetch_all_projects()

for proj in projs:
    YajawConfig.LOGGER.info(f"Return from {__name__}: {proj['key']} -- {proj['name']}")

for _ in range(10):
    projs = jira.fetch_all_projects()

proj = jira.fetch_project(project_key="ABC")
YajawConfig.LOGGER.info(f"Return from {__name__}: {proj['key']} -- {proj['name']}")


projs = jira.search_issues(jql="project in (ABC)")
