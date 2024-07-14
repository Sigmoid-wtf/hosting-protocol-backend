from fastapi import FastAPI, HTTPException

import asyncio
import logging
import os
import shutil

from utils import get_path


app = FastAPI()


@app.post("/create")
async def create(node_id: str):
    os.mkdir(get_path(node_id))

    shutil.copy2("agent/docker-compose.yml", get_path(node_id))

    process = await asyncio.create_subprocess_exec(
        "docker-compose",
        "up",
        "-d",
        cwd=get_path(node_id),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await process.wait()

    logging.info(f"Started node {node_id}")


@app.post("/stop")
async def stop(node_id: str):
    if not os.path.isdir(get_path(node_id)):
        raise HTTPException(status_code=404, detail="node not found")

    process = await asyncio.create_subprocess_exec(
        "docker-compose",
        "down",
        cwd=get_path(node_id),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await process.wait()

    shutil.rmtree(get_path(node_id))
    logging.info(f"Removed node {node_id}")
