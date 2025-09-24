import os
from dotenv import load_dotenv
from jenkinsapi.jenkins import Jenkins
from mcp.server.fastmcp import FastMCP
import logging
import asyncio

logger = logging.getLogger(__name__)

load_dotenv()

JENKINS_URL = os.getenv("JENKINS_URL")
JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")

mcp = FastMCP("jenkins", host="0.0.0.0", port=8931)

jenkins = Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_TOKEN, timeout=1000)

def jenkins_build_job(project, tag: str, params: dict):
    job_name = f"{project}/{tag}"

    # jenkins.build_job(job_name, params) # this will submit jenkins job without watiting for it to complete

    if not jenkins.has_job(job_name):
        raise RuntimeError(f"Job {job_name} does not exist")
    
    job = jenkins.get_job(job_name)
    qi = job.invoke(build_params=params)
    resp = f"start to build job: {job_name}\n"
    if qi.is_queued() or qi.is_running():
        resp += f"build job {job_name} is running\n"
        qi.block_until_complete()

    build = qi.get_build()
    resp += f"build job {job_name} is complete, duration: {build.get_duration()}"
    logger.info(f"{resp}")
    return resp

@mcp.tool()
def build_jenkins_job(project, tag: str, params: dict) -> str:
    """Using Jenkins to build image by project, tag and arch.

    Args:
        project: Jenkins project name
        tag: Jenkins project tag
        params: Jenkins project params, should be a valid python dict object, such as {"arch": "amd64"}, arch can be "amd64" or "arm64"
    """
    
    try:
        jenkins_build_job(project, tag, params)
    except Exception as e:
        return f"Failed to build image: {e}"
    
    return "Jenkins image build successfully"

@mcp.prompt()
def build_jenkins_job_prompt() -> str:
    return "help me start jenkins task"

if __name__ == "__main__":
    # mcp.run(transport="stdio")

    asyncio.run(mcp.run_streamable_http_async())
