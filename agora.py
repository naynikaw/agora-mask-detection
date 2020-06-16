import asyncio
import os
import threading
import time
from asyncio.events import AbstractEventLoop
from io import BytesIO
from pathlib import Path
from threading import Lock
from typing import List, Optional, Callable, Any, Generic, TypeVar

import selenium.webdriver.support.ui as ui
from PIL import Image
from selenium import webdriver

T = TypeVar('T')


def run_async_code(function: Callable[..., Any], loop: AbstractEventLoop) -> Any:
    return loop.run_until_complete(function())


class Cache(Generic[T]):
    call_count: int
    window: int
    capacity: int
    cache_list: List[T]

    def __init__(self, capacity: int = 20, window: int = 10):
        self.cache_list = []
        self.capacity = capacity
        self.window = window
        self.call_count = 0

    def add(self, value: T) -> bool:
        self.cache_list.append(value)
        cache_length: int = len(self.cache_list)

        if cache_length > self.capacity:
            self.cache_list.pop(0)

        self.call_count += 1

        if self.call_count > self.window:
            self.call_count = 0
            return self.reload_needed()

        return False

    def reload_needed(self) -> bool:
        cache_length = len(self.cache_list)
        last_few_frames = self.cache_list[cache_length - self.window:]
        return all([frame == last_few_frames[0] for frame in last_few_frames])


class User:
    def __init__(self, wd, element):
        self.element = element
        self.wd = wd

    @property
    def frame(self):
        x = self.wd.get_screenshot_as_png()
        location = self.element.location
        size = self.element.size
        im = Image.open(BytesIO(x))

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        im = im.crop((left, top, right, bottom))
        return im

    @property
    def id(self):
        return self.element.get_attribute("id")[5:]


class Locker:
    value: Any
    lock: Lock

    def __init__(self, value: Any):
        self.lock = threading.Lock()
        self.value = value


class FrameThread(threading.Thread):
    delay: float
    proc: Callable[..., Any]
    index: int

    def __init__(self, index: int, process: Callable[..., Any], delay: float):
        super().__init__()
        self.index = index
        self.proc = process  # type: ignore
        self.delay = delay

    def run(self) -> None:
        time.sleep(self.index * self.delay)
        self.proc()


class AgoraRTC:
    def __init__(self, app_id: str, loop: AbstractEventLoop, executable: Optional[str] = None, debug: bool = False):
        self.app_id = app_id
        self.channel_name = ""
        self.loop = loop
        self.browser = None
        self.page = None
        self.fps = None
        self.watching = False
        self.executable = executable
        self.debug = debug
        self.wd = None

    @classmethod
    def create_watcher(cls, app_id: str, executable: Optional[str] = None):
        loop = asyncio.get_event_loop()
        return AgoraRTC(app_id, loop, executable)

    def creator(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-user-media-security=true")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--autoplay-policy=no-user-gesture-required")
        if self.executable is None:
            wd = webdriver.Chrome("chromedriver", options=options)
        else:
            wd = webdriver.Chrome(self.executable, options=options)
        wd.get(f'file://{str(Path(os.path.dirname(os.path.realpath(__file__))) / "frontend/index.html")}')
        _ = wd.execute_script(f"bootstrap('{self.app_id}', '{self.channel_name}')")
        wait = ui.WebDriverWait(wd, 10)
        wait.until(lambda driver: driver.find_element_by_class_name("playing"))
        self.wd = wd

    def join_channel(self, channel_name: str):
        self.channel_name = channel_name
        self.creator()

    def close(self):
        self.wd.close()

    def unwatch(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unwatch()

    def get_users_list(self):
        return self.wd.find_elements_by_class_name("playing")

    def get_users(self) -> List[User]:
        return [User(self.wd, i) for i in self.get_users_list()]