
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from get_data import (
    board_semi_F4,
    board_building_F4,
    board_curing_F4,
)


# =========================
# 日 志
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("f4")


# =========================
# 缓存
# =========================

cache = {
    "building": {
        "data": [],
        "status": [],
        "update_time": None,
    },

    "curing": {
        "data": [],
        "status": [],
        "update_time": None,
    },

    "semi": {
        "data": [],
        "status": [],
        "update_time": None,
    },
}


# =========================
# 更新 Building 数据
# =========================

def update_building():

    try:

        data_list, status_list = board_building_F4()

        cache["building"]["data"] = data_list
        cache["building"]["status"] = status_list
        cache["building"]["update_time"] = datetime.now()

        logger.info("Building 数据更新成功")

    except Exception:

        logger.exception("Building 数据更新失败")


# =========================
# 更新 Curing 数据
# =========================

def update_curing():

    try:

        data_list, status_list = board_curing_F4()

        cache["curing"]["data"] = data_list
        cache["curing"]["status"] = status_list
        cache["curing"]["update_time"] = datetime.now()

        logger.info("Curing 数据更新成功")

    except Exception:

        logger.exception("Curing 数据更新失败")


# =========================
# 更新 Semi 数据
# =========================

def update_semi():

    try:

        data_list, status_list = board_semi_F4()

        cache["semi"]["data"] = data_list
        cache["semi"]["status"] = status_list
        cache["semi"]["update_time"] = datetime.now()

        logger.info("Semi 数据更新成功")

    except Exception:

        logger.exception("Semi 数据更新失败")


# =========================
# 更新全部数据
# =========================

def update_all_data():

    logger.info("开始更新 F4 数据")

    update_building()
    update_curing()
    update_semi()

    logger.info("F4 数据更新完成")


# =========================
# 后台定时更新
# =========================

async def update_loop():

    while True:

        try:

            # 把同步的 MES 请求放到线程里
            await asyncio.to_thread(update_all_data)

        except Exception:

            logger.exception("F4 数据更新异常")

        # 30 秒更新一次
        await asyncio.sleep(30)


# =========================
# FastAPI 启动 / 关闭
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("F4 服务启动")

    # 启动时先获取一次数据
    await asyncio.to_thread(update_all_data)

    # 启动后台更新任务
    task = asyncio.create_task(update_loop())

    yield

    # FastAPI 关闭时停止任务
    task.cancel()

    logger.info("F4 服务关闭")


app = FastAPI(lifespan=lifespan)


# =========================
# 静态文件
# =========================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


templates = Jinja2Templates(directory="templates")


# =========================
# 页面 1：Building
# =========================

@app.get("/f4/page1")
def page1(request: Request):

    return templates.TemplateResponse(
        "building.html",
        {
            "request": request,
            "list": cache["building"]["data"],
            "status_list": cache["building"]["status"],
            "update_time": cache["building"]["update_time"],
        },
    )


# =========================
# 页面 2：Curing
# =========================

@app.get("/f4/page2")
def page2(request: Request):

    return templates.TemplateResponse(
        "curing.html",
        {
            "request": request,
            "list": cache["curing"]["data"],
            "status_list": cache["curing"]["status"],
            "update_time": cache["curing"]["update_time"],
        },
    )


# =========================
# 页面 3：Semi
# =========================

@app.get("/f4/page3")
def page3(request: Request):

    return templates.TemplateResponse(
        "semi.html",
        {
            "request": request,
            "list": cache["semi"]["data"],
            "status_list": cache["semi"]["status"],
            "update_time": cache["semi"]["update_time"],
        },
    )
