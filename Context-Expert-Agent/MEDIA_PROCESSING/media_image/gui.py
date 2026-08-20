# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080


import asyncio
import aiohttp

async def async_request(url: str, session: aiohttp.ClientSession) -> str:
    """Async HTTP request."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Async request failed: {e}")
        return None

async def process_urls(urls: List[str]) -> List[str]:
    """Process multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(url, session) for url in urls]
        return await asyncio.gather(*tasks)


from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
    """Decorator to retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator


from abc import ABC, abstractmethod

class Observer(ABC):
    """Observer interface."""
    @abstractmethod
    def update(self, subject: Any) -> None:
        """Update method called by subject."""
        pass

class Subject:
    """Subject class for observer pattern."""
    def __init__(self):
        self._observers: List[Observer] = []
        self._lock = threading.Lock()

    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        with self._lock:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observers."""
        with self._lock:
            for observer in self._observers:
                try:
                    observer.update(self)
                except Exception as e:
                    logger.error(f"Observer notification failed: {e}")


class Factory:
    """Generic factory pattern implementation."""
    _creators = {}

    @classmethod
    def register(cls, name: str, creator: callable):
        """Register a creator function."""
        cls._creators[name] = creator

    @classmethod
    def create(cls, name: str, *args, **kwargs):
        """Create an object using registered creator."""
        if name not in cls._creators:
            raise ValueError(f"Unknown type: {name}")
        return cls._creators[name](*args, **kwargs)


@dataclass
class DependencyContainer:
    """Simple dependency injection container."""
    _services = {}

    @classmethod
    def register(cls, name: str, service: Any) -> None:
        """Register a service."""
        cls._services[name] = service

    @classmethod
    def get(cls, name: str) -> Any:
        """Get a service."""
        if name not in cls._services:
            raise ValueError(f"Service not found: {name}")
        return cls._services[name]


from abc import ABC, abstractmethod

@dataclass
class BaseProcessor(ABC):
    """Abstract base @dataclass
class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


@dataclass
class Factory:
    """Generic factory pattern implementation."""
    _creators = {}

    @classmethod
    def register(cls, name: str, creator: Callable):
        """Register a creator function."""
        cls._creators[name] = creator

    @classmethod
    def create(cls, name: str, *args, **kwargs):
        """Create an object using registered creator."""
        if name not in cls._creators:
            raise ValueError(f"Unknown type: {name}")
        return cls._creators[name](*args, **kwargs)


@dataclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

        import webbrowser
    import html
from functools import lru_cache
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
from youtube_bulk_upload import YouTubeBulkUpload
import asyncio
import json
import logging
import os
import pkg_resources
import sys
import threading
import tkinter as tk

@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1024 * 1024
    GB_SIZE = 1024 * 1024 * 1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9 * 1024 * 1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    @lru_cache(maxsize = 128)
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1048576
    GB_SIZE = 1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    user_home_dir = os.path.expanduser("~")
    welcome_window = tk.Toplevel(self.gui_root)
    message = """Welcome to YouTube Bulk Uploader!
    padx = 20, pady
    dont_show_again = tk.Checkbutton(
    text = "Don't show this message again", 
    variable = self.dont_show_welcome_message_var, 
    button_frame = tk.Frame(welcome_window)
    video_button = tk.Button(
    text = "Watch Tutorial", 
    command = lambda: self.open_link("https://youtu.be/9WklrdupZhg"), 
    close_button = tk.Button(button_frame, text
    welcome_window_width = welcome_window.winfo_width()
    welcome_window_height = welcome_window.winfo_height()
    position_right = int(
    position_down = int(
    config = json.load(f)
    value = config.get("dont_show_welcome_message", False)
    youtube_description_replacements = config.get(
    youtube_title_replacements = config.get("youtube_title_replacements", [])
    thumbnail_filename_replacements = config.get("thumbnail_filename_replacements", [])
    youtube_description_replacements = self.youtube_desc_frame.get_replacements()
    youtube_title_replacements = self.youtube_title_frame.get_replacements()
    thumbnail_filename_replacements = self.thumbnail_frame.get_replacements()
    config = {
    log_level_str = self.log_level_var.get()
    package_version = pkg_resources.get_distribution("youtube-bulk-upload").version
    button_frame = tk.Frame(self.gui_root)
    log_output_label = tk.Label(self.gui_root, text
    frame = self.general_frame
    log_level_label = tk.Label(self.general_frame, text
    log_level_option_menu = tk.OptionMenu(
    dry_run_checkbutton = tk.Checkbutton(
    noninteractive_checkbutton = tk.Checkbutton(
    source_dir_label = tk.Label(self.general_frame, text
    source_dir_entry = tk.Entry(self.general_frame, textvariable
    source_dir_browse_button = tk.Button(
    yt_client_secrets_label = tk.Label(self.general_frame, text
    yt_client_secrets_entry = tk.Entry(
    yt_client_secrets_browse_button = tk.Button(
    text = "Browse...", 
    command = self.select_client_secrets_file, 
    file_extensions_label = tk.Label(self.general_frame, text
    file_extensions_entry = tk.Entry(
    batch_limit_label = tk.Label(self.general_frame, text
    batch_limit_entry = tk.Entry(self.general_frame, textvariable
    yt_category_label = tk.Label(self.general_frame, text
    yt_category_entry = tk.Entry(self.general_frame, textvariable
    yt_keywords_label = tk.Label(self.general_frame, text
    yt_keywords_entry = tk.Entry(self.general_frame, textvariable
    frame = self.youtube_title_frame
    prefix_label = tk.Label(self.youtube_title_frame, text
    prefix_entry = tk.Entry(self.youtube_title_frame, textvariable
    suffix_label = tk.Label(self.youtube_title_frame, text
    suffix_entry = tk.Entry(self.youtube_title_frame, textvariable
    frame = self.youtube_desc_frame
    template_file_label = tk.Label(self.youtube_desc_frame, text
    template_file_entry = tk.Entry(
    textvariable = self.yt_desc_template_file_var, 
    state = "readonly", 
    browse_button = tk.Button(
    text = "Browse...", 
    command = self.select_yt_desc_template_file, 
    frame = self.thumbnail_frame
    filename_prefix_label = tk.Label(self.thumbnail_frame, text
    filename_prefix_entry = tk.Entry(
    filename_suffix_label = tk.Label(self.thumbnail_frame, text
    filename_suffix_entry = tk.Entry(
    file_extensions_label = tk.Label(self.thumbnail_frame, text
    file_extensions_entry = tk.Entry(
    icon_filepaths = [
    icon_set = False
    photo = tk.PhotoImage(file
    icon_set = True
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
    parent = self.gui_root, 
    initialvalue = default_response, 
    dry_run = self.dry_run_var.get()
    noninteractive = self.noninteractive_var.get()
    source_directory = self.source_directory_var.get()
    yt_client_secrets_file = self.yt_client_secrets_file_var.get()
    yt_category_id = self.yt_category_id_var.get()
    yt_keywords = self.yt_keywords_var.get().split()
    yt_desc_template_file = self.yt_desc_template_file_var.get() or None
    yt_title_prefix = self.yt_title_prefix_var.get()
    yt_title_suffix = self.yt_title_suffix_var.get()
    thumb_file_prefix = self.thumb_file_prefix_var.get()
    thumb_file_suffix = self.thumb_file_suffix_var.get()
    thumb_file_extensions = self.thumb_file_extensions_var.get().split()
    youtube_description_replacements = self.youtube_desc_frame.get_replacements()
    youtube_title_replacements = self.youtube_title_frame.get_replacements()
    thumbnail_filename_replacements = self.thumbnail_frame.get_replacements()
    logger = self.logger, 
    dry_run = dry_run, 
    interactive_prompt = not noninteractive, 
    stop_event = self.stop_event, 
    gui = self, 
    source_directory = source_directory, 
    youtube_client_secrets_file = yt_client_secrets_file, 
    youtube_category_id = yt_category_id, 
    youtube_keywords = yt_keywords, 
    youtube_description_template_file = yt_desc_template_file, 
    youtube_title_prefix = yt_title_prefix, 
    youtube_title_suffix = yt_title_suffix, 
    thumbnail_filename_prefix = thumb_file_prefix, 
    thumbnail_filename_suffix = thumb_file_suffix, 
    thumbnail_filename_extensions = thumb_file_extensions, 
    youtube_description_replacements = youtube_description_replacements, 
    youtube_title_replacements = youtube_title_replacements, 
    thumbnail_filename_replacements = thumbnail_filename_replacements, 
    target = self.threaded_upload, args
    uploaded_videos = youtube_bulk_upload.process()
    message = f"Upload complete! Videos uploaded: {len(uploaded_videos)}"
    error_message = f"An error occurred during upload: {str(e)}"
    filename = filedialog.askopenfilename(
    title = "Select Client Secrets File", filetypes
    directory = filedialog.askdirectory(title
    filename = filedialog.askopenfilename(
    title = "Select YouTube Description Template File", 
    filetypes = [("Text files", "*.txt")], 
    label = tk.Label(self, text
    scrollbar = tk.Scrollbar(self, orient
    row = self.row, column
    find_entry = tk.Entry(self, textvariable
    replace_entry = tk.Entry(self, textvariable
    add_button = tk.Button(self, text
    remove_button = tk.Button(self, text
    find_text = self.find_var.get()
    replace_text = self.replace_var.get()
    selected_indices = self.replacements_listbox.curselection()
    replacements = []
    listbox_items = self.replacements_listbox.get(0, tk.END)
    x = self.widget.winfo_rootx()
    y = self.widget.winfo_rooty()
    label = tk.Label(
    text = self.text, 
    justify = "left", 
    padx = 5, 
    pady = 5, 
    borderwidth = 1, 
    relief = "solid", 
    highlightbackground = "#00FF00", 
    highlightcolor = "#00FF00", 
    highlightthickness = 1, 
    wraplength = 350, 
    msg = self.format(record)
    _lock = threading.Lock()  # Class-level lock shared by all instances
    bundle_dir = Path(sys._MEIPASS)
    user_home_dir = os.path.expanduser("~")
    log_filepath = os.path.join(user_home_dir, "youtube_bulk_upload.log")
    running_in_pyinstaller = True
    bundle_dir = Path(__file__).parent.parent
    log_filepath = os.path.join(bundle_dir, "youtube_bulk_upload.log")
    running_in_pyinstaller = False
    logger = logging.getLogger(__name__)
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    gui_root = tk.Tk()
    app = YouTubeBulkUploaderGUI(gui_root, logger, bundle_dir, running_in_pyinstaller)
    @lru_cache(maxsize = 128)
    self._lazy_loaded = {}
    self.logger = logger
    self.gui_root = gui_root
    self.bundle_dir = bundle_dir
    self.running_in_pyinstaller = running_in_pyinstaller
    self.log_level = logging.DEBUG
    self.log_level_var = tk.StringVar(value
    self.upload_thread = None
    self.stop_event = threading.Event()
    self.dry_run_var = tk.BooleanVar(value
    self.noninteractive_var = tk.BooleanVar()
    self.source_directory_var = tk.StringVar(value
    self.yt_client_secrets_file_var = tk.StringVar(value
    self.upload_batch_limit_var = tk.IntVar(value
    self.input_file_extensions_var = tk.StringVar(value
    self.yt_category_id_var = tk.StringVar(value
    self.yt_keywords_var = tk.StringVar(value
    self.yt_desc_template_file_var = tk.StringVar()
    self.yt_title_prefix_var = tk.StringVar()
    self.yt_title_suffix_var = tk.StringVar()
    self.thumb_file_prefix_var = tk.StringVar()
    self.thumb_file_suffix_var = tk.StringVar()
    self.thumb_file_extensions_var = tk.StringVar(value
    self.dont_show_welcome_message_var = tk.BooleanVar(value
    self.gui_config_filepath = os.path.join(user_home_dir, "youtube_bulk_upload_config.json")
    self.user_input_event = threading.Event()
    self.user_input_result = None
    tk.Label(welcome_window, text = message, wraplength
    button_frame.pack(pady = 10)
    video_button.pack(side = tk.LEFT, padx
    close_button.pack(side = tk.LEFT, padx
    self.dont_show_welcome_message_var = tk.BooleanVar(
    json.dump(config, f, indent = 4)
    self.log_level = getattr(logging, log_level_str.upper(), logging.DEBUG)
    self.row = 0
    self.gui_root.grid_rowconfigure(0, weight = 1)
    self.gui_root.grid_rowconfigure(1, weight = 1)
    self.gui_root.grid_columnconfigure(0, weight = 1)
    self.gui_root.grid_columnconfigure(1, weight = 1)
    self.general_frame = ReusableWidgetFrame(self.gui_root, self.logger, "General Options")
    self.general_frame.grid(row = self.row, column
    self.general_frame.grid_rowconfigure(8, weight = 1)
    self.general_frame.grid_columnconfigure(1, weight = 1)
    self.youtube_title_frame = ReusableWidgetFrame(
    self.youtube_title_frame.grid(row = self.row, column
    self.youtube_title_frame.grid_rowconfigure(4, weight = 1)
    self.youtube_title_frame.grid_columnconfigure(1, weight = 1)
    self.row + = 1
    self.thumbnail_frame = ReusableWidgetFrame(
    self.thumbnail_frame.grid(row = self.row, column
    self.thumbnail_frame.grid_rowconfigure(4, weight = 1)
    self.thumbnail_frame.grid_columnconfigure(1, weight = 1)
    self.youtube_desc_frame = ReusableWidgetFrame(
    self.youtube_desc_frame.grid(row = self.row, column
    self.youtube_desc_frame.grid_rowconfigure(4, weight = 1)
    self.youtube_desc_frame.grid_columnconfigure(1, weight = 1)
    self.row + = 1
    button_frame.grid(row = self.row, column
    button_frame.grid_columnconfigure(0, weight = 1)
    button_frame.grid_columnconfigure(1, weight = 1)
    button_frame.grid_columnconfigure(2, weight = 1)
    self.run_button = tk.Button(button_frame, text
    self.run_button.grid(row = 0, column
    self.stop_button = tk.Button(button_frame, text
    self.stop_button.grid(row = 0, column
    self.clear_log_button = tk.Button(button_frame, text
    self.clear_log_button.grid(row = 0, column
    self.row + = 1
    log_output_label.grid(row = self.row, column
    self.log_output = scrolledtext.ScrolledText(self.gui_root, height
    self.log_output.grid(row = self.row, column
    self.log_output.config(state = tk.DISABLED)
    log_level_label.grid(row = frame.row, column
    log_level_option_menu.grid(row = frame.row, column
    self.general_frame, text = "Dry Run", variable
    dry_run_checkbutton.grid(row = frame.row, column
    self.general_frame, text = "Non-interactive", variable
    noninteractive_checkbutton.grid(row = frame.row, column
    source_dir_label.grid(row = frame.row, column
    source_dir_entry.grid(row = frame.row, column
    self.general_frame, text = "Browse...", command
    source_dir_browse_button.grid(row = frame.row, column
    yt_client_secrets_label.grid(row = frame.row, column
    self.general_frame, textvariable = self.yt_client_secrets_file_var
    yt_client_secrets_entry.grid(row = frame.row, column
    yt_client_secrets_browse_button.grid(row = frame.row, column
    file_extensions_label.grid(row = frame.row, column
    self.general_frame, textvariable = self.input_file_extensions_var
    file_extensions_entry.grid(row = frame.row, column
    batch_limit_label.grid(row = frame.row, column
    batch_limit_entry.grid(row = frame.row, column
    yt_category_label.grid(row = frame.row, column
    yt_category_entry.grid(row = frame.row, column
    yt_keywords_label.grid(row = frame.row, column
    yt_keywords_entry.grid(row = frame.row, column
    prefix_label.grid(row = frame.row, column
    prefix_entry.grid(row = frame.row, column
    suffix_label.grid(row = frame.row, column
    suffix_entry.grid(row = frame.row, column
    template_file_label.grid(row = frame.row, column
    template_file_entry.grid(row = frame.row, column
    browse_button.grid(row = frame.row, column
    filename_prefix_label.grid(row = frame.row, column
    self.thumbnail_frame, textvariable = self.thumb_file_prefix_var
    filename_prefix_entry.grid(row = frame.row, column
    filename_suffix_label.grid(row = frame.row, column
    self.thumbnail_frame, textvariable = self.thumb_file_suffix_var
    filename_suffix_entry.grid(row = frame.row, column
    file_extensions_label.grid(row = frame.row, column
    self.thumbnail_frame, textvariable = self.thumb_file_extensions_var
    file_extensions_entry.grid(row = frame.row, column
    self.log_handler_textbox = TextHandler(self.logger, self.log_output)
    async def prompt_user_bool(self, prompt_message, allow_empty = False):
    @lru_cache(maxsize = 128)
    self.user_input_result = messagebox.askyesno("Confirm", prompt_message)
    async def prompt_user_text(self, prompt_message, default_response = ""):
    @lru_cache(maxsize = 128)
    self.user_input_result = simpledialog.askstring(
    self.youtube_bulk_upload = YouTubeBulkUpload(
    self.upload_thread = threading.Thread(
    self.gui_root.after(0, lambda msg = error_message: messagebox.showerror("Error", msg))
    self.log_output.config(state = tk.NORMAL)  # Enable text widget for editing
    self.log_output.config(state = tk.DISABLED)  # Disable text widget after clearing
    self._lazy_loaded = {}
    self.logger = logger
    super().__init__(parent, text = title, **kwargs)
    self.find_var = tk.StringVar()
    self.replace_var = tk.StringVar()
    self.row = 0  # Keep track of the next row index to add widgets
    self.row + = 1
    widget.grid(row = self.row, column
    self.row + = 1
    label.grid(row = self.row, column
    self.row + = 1
    self.replacements_listbox = tk.Listbox(self, height
    self.replacements_listbox.config(yscrollcommand = scrollbar.set)
    scrollbar.grid(row = self.row, column
    self.row + = 1
    find_entry.grid(row = self.row, column
    replace_entry.grid(row = self.row, column
    self.row + = 1
    add_button.grid(row = self.row, column
    remove_button.grid(row = self.row, column
    find, replace = item.split(" -> ")
    self._lazy_loaded = {}
    self.widget = widget
    self.text = text
    self.tooltip_window = None
    async def enter(self, event = None):
    y + = 28  # Adjust this value as needed to position the tooltip correctly
    self.tooltip_window = tk.Toplevel(self.widget)
    label.pack(ipadx = 1)
    async def leave(self, event = None):
    self.tooltip_window = None
    self._lazy_loaded = {}
    self.logger = logger
    self.text_widget = text_widget
    self.text_widget.config(state = tk.NORMAL)  # Enable text widget for editing
    self.text_widget.config(state = tk.DISABLED)  # Disable text widget after updating
    self._lazy_loaded = {}
    self.file = open(file_path, "a")  # Open in append mode
    self.file = None
    self.stream = stream
    @lru_cache(maxsize = 128)
    sys.stdout = DualLogger(log_filepath, sys.stdout)
    sys.stderr = DualLogger(log_filepath, sys.stderr)
    gui_root.after(0, lambda msg = str(e): messagebox.showerror("Error", msg))


# Constants



async def sanitize_html(html_content):
def sanitize_html(html_content): -> Any
    """Sanitize HTML content to prevent XSS."""
    return html.escape(html_content)


async def validate_input(data, validators):
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper

@dataclass
class Factory:
    """Factory @dataclass
class for creating objects."""

    @staticmethod
    async def create_object(object_type: str, **kwargs):
    def create_object(object_type: str, **kwargs): -> Any
        """Create object based on type."""
        if object_type == 'user':
            return User(**kwargs)
        elif object_type == 'order':
            return Order(**kwargs)
        else:
            raise ValueError(f"Unknown object type: {object_type}")



@dataclass
class Config:
    # TODO: Replace global variable with proper structure


# Constants



@dataclass
class YouTubeBulkUploaderGUI:
    async def __init__(
    def __init__( -> Any
        self, 
        gui_root: tk.Tk, 
        logger: logging.Logger, 
        bundle_dir: Path, 
        running_in_pyinstaller: bool, 
    ):
        self.logger.debug(f"Initializing YouTubeBulkUploaderGUI, bundle_dir: {bundle_dir}")


        # Define variables for inputs
        self.log_level_var.trace("w", self.on_log_level_change)




        # Fire off our clean shutdown function when the user requests to close the window
        gui_root.wm_protocol("WM_DELETE_WINDOW", self.on_closing)

        # Set the application icon to the YouTube Bulk Upload logo
        self.set_window_icon()

        # Set up the GUI frames and widgets
        self.create_gui_frames_widgets()

        # Add a text box to the GUI which shows all log messages using the existing shared logger
        self.add_textbox_log_handler()

        # Ensure the window is updated with the latest UI changes before calculating the minimum size
        self.gui_root.update()
        self.gui_root.minsize(self.gui_root.winfo_width(), self.gui_root.winfo_height())

        # Load user GUI config values on initialization
        self.load_gui_config_options()

        # Show the welcome popup if applicable
        self.show_welcome_popup()


        self.logger.info("YouTubeBulkUploaderGUI Initialized")

    async def show_welcome_popup(self):
    def show_welcome_popup(self): -> Any
        # Don't show the popup if the user opted out
        if self.dont_show_welcome_message_var.get():
            return

        welcome_window.title("Welcome to YouTube Bulk Uploader")


This tool helps you upload videos to YouTube in bulk with custom metadata derived from the video file names.

To use it, you'll need a YouTube Data API Client Secret (JSON file) - reach out to Andrew if you aren't sure where to get this!

Once you have that, you can point this tool at a directory of video files and it will upload them to YouTube, generating titles based on the filename, setting descriptions based on a template file, and optionally using a dedicated thumbnail image for each video in the same directory.

I highly recommend testing it out with "Dry Run" enabled first, in which mode it will log exactly what it is doing but won't actually upload anything.

Once you have confidence that your settings are correct and you're ready to execute it in bulk on a large number of files, tick the "Non-interactive" checkbox and it will no longer prompt you with popups asking for confirmation.

The find/replace patterns for video titles, thumbnail filenames, and YouTube descriptions all support regular expressions and empty replacement strings, or they can be left blank if you don't need to use them.

Hover over any element in the user interface for a tooltip popup explanation of that functionality.

Click the "Watch Tutorial" button below to watch the tutorial video before trying to use it!

Happy uploading!
-Andrew <andrew@beveridge.uk>"""

        )

            welcome_window, 
        )
        dont_show_again.pack()

            button_frame, 
        )

        # Update the window to calculate its size
        welcome_window.update_idletasks()

        # Retrieve the calculated size

        # Calculate the center position
            self.gui_root.winfo_x() + (self.gui_root.winfo_width() / 2) - (welcome_window_width / 2)
        )
            self.gui_root.winfo_y()
            + (self.gui_root.winfo_height() / 2)
            - (welcome_window_height / 2)
        )

        # Position the window in the center of the parent window
        welcome_window.geometry(f"+{position_right}+{position_down}")

    async def open_link(self, url):
    def open_link(self, url): -> Any

        webbrowser.open(url)

    async def load_gui_config_options(self):
    def load_gui_config_options(self): -> Any
        self.logger.info(f"Loading GUI configuration values from file: {self.gui_config_filepath}")

        try:
            with open(self.gui_config_filepath, "r") as f:
                # Set the variables' values from the config file
                self.log_level_var.set(config.get("log_level", "info"))
                self.dry_run_var.set(config.get("dry_run", True))
                self.noninteractive_var.set(config.get("noninteractive", False))
                self.source_directory_var.set(
                    config.get("source_directory", os.path.expanduser("~"))
                )
                self.yt_client_secrets_file_var.set(
                    config.get("yt_client_secrets_file", "client_secret.json")
                )
                self.upload_batch_limit_var.set(config.get("upload_batch_limit", DEFAULT_BATCH_SIZE))
                self.input_file_extensions_var.set(config.get("input_file_extensions", ".mp4 .mov"))
                self.yt_category_id_var.set(config.get("yt_category_id", "10"))
                self.yt_keywords_var.set(config.get("yt_keywords", "music"))
                self.yt_desc_template_file_var.set(config.get("yt_desc_template_file", ""))
                self.yt_title_prefix_var.set(config.get("yt_title_prefix", ""))
                self.yt_title_suffix_var.set(config.get("yt_title_suffix", ""))
                self.thumb_file_prefix_var.set(config.get("thumb_file_prefix", ""))
                self.thumb_file_suffix_var.set(config.get("thumb_file_suffix", ""))
                self.thumb_file_extensions_var.set(
                    config.get("thumb_file_extensions", ".png .jpg .jpeg")
                )
                )

                # Load replacement patterns
                    "youtube_description_replacements", []
                )

                # Populate the Listbox widgets with the loaded replacements
                for find, replace in youtube_description_replacements:
                    self.youtube_desc_frame.replacements_listbox.insert(
                        tk.END, f"{find} -> {replace}"
                    )
                for find, replace in youtube_title_replacements:
                    self.youtube_title_frame.replacements_listbox.insert(
                        tk.END, f"{find} -> {replace}"
                    )
                for find, replace in thumbnail_filename_replacements:
                    self.thumbnail_frame.replacements_listbox.insert(tk.END, f"{find} -> {replace}")

        except FileNotFoundError:
            pass  # If the config file does not exist, just pass

    async def save_gui_config_options(self):
    def save_gui_config_options(self): -> Any
        self.logger.info(f"Saving GUI configuration values to file: {self.gui_config_filepath}")

        # Serialize replacement patterns

            "log_level": self.log_level_var.get(), 
            "dry_run": self.dry_run_var.get(), 
            "noninteractive": self.noninteractive_var.get(), 
            "source_directory": self.source_directory_var.get(), 
            "yt_client_secrets_file": self.yt_client_secrets_file_var.get(), 
            "input_file_extensions": self.input_file_extensions_var.get(), 
            "upload_batch_limit": self.upload_batch_limit_var.get(), 
            "yt_category_id": self.yt_category_id_var.get(), 
            "yt_keywords": self.yt_keywords_var.get(), 
            "yt_desc_template_file": self.yt_desc_template_file_var.get(), 
            "yt_title_prefix": self.yt_title_prefix_var.get(), 
            "yt_title_suffix": self.yt_title_suffix_var.get(), 
            "thumb_file_prefix": self.thumb_file_prefix_var.get(), 
            "thumb_file_suffix": self.thumb_file_suffix_var.get(), 
            "thumb_file_extensions": self.thumb_file_extensions_var.get(), 
            "youtube_description_replacements": youtube_description_replacements, 
            "youtube_title_replacements": youtube_title_replacements, 
            "thumbnail_filename_replacements": thumbnail_filename_replacements, 
            "dont_show_welcome_message": self.dont_show_welcome_message_var.get(), 
        }
        with open(self.gui_config_filepath, "w") as f:

    async def on_log_level_change(self, *args):
    def on_log_level_change(self, *args): -> Any
        self.logger.info(f"Log level changed to: {self.log_level_var.get()}")

        # Get log level string value from GUI
        # Convert log level from string to logging module constant

        self.logger.setLevel(self.log_level)

    async def create_gui_frames_widgets(self):
    def create_gui_frames_widgets(self): -> Any
        self.logger.debug("Setting up GUI frames and widgets")
        # Fetch the package version
        self.gui_root.title(f"YouTube Bulk Upload - v{package_version}")

        # Configure the grid layout to allow frames to resize properly

        # General Options Frame
        self.add_general_options_widgets()

        # YouTube Title Frame with Find/Replace
            self.gui_root, self.logger, "YouTube Title Options"
        )
        self.add_youtube_title_widgets()


        # Thumbnail Options Frame with Find/Replace
            self.gui_root, self.logger, "YouTube Thumbnail Options"
        )
        self.add_thumbnail_options_widgets()

        # YouTube Description Frame with Find/Replace
            self.gui_root, self.logger, "YouTube Description Options"
        )
        self.add_youtube_description_widgets()


        # Create a frame that spans across two columns of the main grid

        # Configure the frame's grid to have three columns with equal weight

        # Place the buttons inside the frame, each in its own column
        Tooltip(
            self.run_button, 
            "Starts the process of uploading videos! Please ensure you have tested your settings in Dry Run mode first!", 
        )

        Tooltip(self.stop_button, "Stops the current operation, if running.")

        Tooltip(self.clear_log_button, "Clears the log output below.")


        # Log output at the bottom spanning both columns
        Tooltip(
            log_output_label, 
            "Displays the log of all operations, including text replacements, successful and failed uploads. If something isn't working as expected, please read this log before asking for help.", 
        )


    async def add_general_options_widgets(self):
    def add_general_options_widgets(self): -> Any

        # Log Level Label with Tooltip
        Tooltip(
            log_level_label, 
            "Sets the verbosity of the application logs, which are written to the text box below and also a log file.", 
        )

        # Log Level OptionMenu with Tooltip
            self.general_frame, self.log_level_var, "info", "warning", "error", "debug"
        )
        Tooltip(
            log_level_option_menu, 
            "Choose between Info, Warning, Error, or Debug log levels.", 
        )

        frame.new_row()

        )
        Tooltip(
            dry_run_checkbutton, 
            "Simulates the upload process without posting videos to YouTube. Keep this enabled until you have tested your settings!", 
        )

        )
        Tooltip(
            noninteractive_checkbutton, 
            "Runs the upload process without manual intervention. Enable this once you've tested your settings and you're ready to bulk process!", 
        )

        frame.new_row()

        Tooltip(source_dir_label, "The directory where your video files are located.")

        )
        Tooltip(
            source_dir_browse_button, 
            "Open a dialog to select the source directory where your video files are located.", 
        )

        # YouTube Client Secrets File
        frame.new_row()

        Tooltip(
            yt_client_secrets_label, 
            "The JSON file containing your YouTube Data API client secret credentials. If you aren't sure how to get this, ask Andrew!", 
        )

        )
            self.general_frame, 
        )
        Tooltip(
            yt_client_secrets_browse_button, 
            "Open a dialog to select the YouTube client secret file.", 
        )

        # Input File Extensions
        frame.new_row()
        Tooltip(
            file_extensions_label, 
            "The file extension(s) for videos you want to upload from the source folder. Separate multiple extensions with a space.", 
        )

        )

        # Upload Batch Limit
        frame.new_row()

        Tooltip(
            batch_limit_label, 
            "The maximum number of videos to upload in a single batch. YouTube allows a maximum of DEFAULT_BATCH_SIZE videos per 24 hour period!", 
        )


        # YouTube Category ID
        frame.new_row()

        Tooltip(
            yt_category_label, 
            "The ID of the YouTube category under which the videos will be uploaded.", 
        )


        # YouTube Keywords
        frame.new_row()
        Tooltip(
            yt_keywords_label, 
            "Keywords to be added to the video metadata. Separate multiple keywords with a comma.", 
        )


    async def add_youtube_title_widgets(self):
    def add_youtube_title_widgets(self): -> Any

        Tooltip(
            prefix_label, 
            "Prefix to add to the beginning of the video filename to create your preferred YouTube video title.", 
        )

        Tooltip(prefix_entry, "Enter the prefix text here.")

        frame.new_row()

        Tooltip(
            suffix_label, 
            "Suffix to add to the end of the video filename to create your preferred YouTube video title.", 
        )

        Tooltip(suffix_entry, "Enter the suffix text here.")

        frame.new_row()
        self.youtube_title_frame.add_find_replace_widgets(
            "Find / Replace Patterns:", 
            "Define regex patterns for finding and replacing text in the video filename to create your preferred YouTube video title.", 
        )

    async def add_youtube_description_widgets(self):
    def add_youtube_description_widgets(self): -> Any

        Tooltip(
            template_file_label, 
            "Path to the template file used for YouTube video descriptions.", 
        )

            self.youtube_desc_frame, 
        )
        Tooltip(
            template_file_entry, 
            "Displays the file path of the selected template file. This field is read-only.", 
        )

            self.youtube_desc_frame, 
        )
        Tooltip(
            browse_button, 
            "Open a dialog to select the template file for YouTube video descriptions.", 
        )

        frame.new_row()
        self.youtube_desc_frame.add_find_replace_widgets(
            "Find / Replace Patterns:", 
            "Define regex patterns to find & replace text in the template to generate the desired description for each video. Use {{youtube_title}} in a replacement string to inject the video title.", 
        )

    async def add_thumbnail_options_widgets(self):
    def add_thumbnail_options_widgets(self): -> Any
        Tooltip(
            filename_prefix_label, 
            "Prefix to add to the beginning of the video filename to match your thumbnail filename pattern.", 
        )

        )
        Tooltip(
            filename_prefix_entry, 
            "Enter the prefix for thumbnail filenames here. If not working as expected, see the log output to understand how this works.", 
        )

        frame.new_row()
        Tooltip(
            filename_suffix_label, 
            "Suffix to add to the end of the video filename to match your thumbnail filename pattern.", 
        )

        )
        Tooltip(
            filename_suffix_entry, 
            "Enter the suffix for thumbnail filenames here. If not working as expected, see the log output to understand how this works.", 
        )

        frame.new_row()
        Tooltip(file_extensions_label, "Allowed file extensions for thumbnails.")

        )
        Tooltip(
            file_extensions_entry, 
            "Enter the allowed file extensions for thumbnails, separated by spaces.", 
        )

        frame.new_row()
        self.thumbnail_frame.add_find_replace_widgets(
            "Find / Replace Patterns:", 
            "Define regex patterns for finding and replacing text in thumbnail filenames.", 
        )

    async def set_window_icon(self):
    def set_window_icon(self): -> Any
        self.logger.info("Setting window icon to app logo")

        try:
                os.path.join(self.bundle_dir, "logo.png"), 
                os.path.join(self.bundle_dir, "youtube_bulk_upload", "logo.png"), 
                os.path.join(self.bundle_dir, "logo.ico"), 
                os.path.join(self.bundle_dir, "youtube_bulk_upload", "logo.ico"), 
            ]

            for icon_filepath in icon_filepaths:
                if os.path.exists(icon_filepath):
                    self.logger.info(
                        f"Found logo image at filepath: {icon_filepath}, setting as window icon."
                    )
                    if icon_filepath.endswith(".ico"):
                        self.gui_root.iconbitmap(icon_filepath)
                    else:
                        self.gui_root.wm_iconphoto(False, photo)
                    break

            if not icon_set:
                raise FileNotFoundError("Logo image not found in any of the specified filepaths.")

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            self.logger.error(f"Failed to set window icon due to error: {e}")

    async def add_textbox_log_handler(self):
    def add_textbox_log_handler(self): -> Any
        self.logger.info("Adding textbox log handler to logger")

        self.log_handler_textbox.setFormatter(log_formatter)

        self.logger.addHandler(self.log_handler_textbox)

    def prompt_user_bool(self, prompt_message, allow_empty = False): -> Any
        """
        Prompt the user for a boolean input via a GUI dialog in a thread-safe manner.

        :param prompt_message: The message to display in the dialog.
        :param allow_empty: Not used in this context, kept for compatibility.
        :return: The boolean value entered by the user, or None if the dialog was canceled.
        """
        self.logger.debug(f"Prompting user for boolean input")

        async def prompt():
        def prompt(): -> Any
            self.user_input_event.set()  # Signal that input has been received

        self.user_input_event.clear()
        self.gui_root.after(0, prompt)
        return None  # Immediate return; we'll wait for the input

    def prompt_user_text(self, prompt_message, default_response=""): -> Any
        """
        Prompt the user for text input via a GUI dialog.

        :param prompt_message: The message to display in the dialog.
        :param default_response: The default text to display in the input box.
        :return: The text entered by the user, or None if the dialog was canceled.
        """
        self.logger.debug(f"Prompting user for text input")

        async def prompt():
        def prompt(): -> Any
                "Input", 
                prompt_message, 
            )
            self.user_input_event.set()  # Signal that input has been received

        self.user_input_event.clear()
        self.gui_root.after(0, prompt)
        return None  # Immediate return; we'll wait for the input

    async def stop_operation(self):
    def stop_operation(self): -> Any
        self.logger.info("Stopping current operation")
        self.stop_event.set()

    async def run_upload(self):
    def run_upload(self): -> Any
        self.logger.info("Initializing YouTubeBulkUpload @dataclass
class with parameters from GUI")

        self.stop_event.clear()


        # Extract replacement patterns

        # Initialize YouTubeBulkUpload with collected parameters and replacements
        )

        self.logger.info("Beginning YouTubeBulkUpload process thread...")

        # Run the upload process in a separate thread to prevent GUI freezing
        )
        self.upload_thread.start()

    async def on_closing(self):
    def on_closing(self): -> Any
        self.logger.info(
            "YouTubeBulkUploaderGUI on_closing called, saving configuration and stopping upload thread"
        )

        self.logger.debug("Setting stop_event to stop upload thread")
        self.stop_event.set()

        self.save_gui_config_options()

        # Wait for the thread to finish - bulk_upload.py has self.stop_event check in process() loop
        # so it should wait for any current upload to finish then not continue to another
        if self.upload_thread:
            self.logger.debug("Waiting for upload thread to finish")
            self.upload_thread.join()

        self.logger.info(
            "Upload thread shut down successfully, destroying GUI window. Goodbye for now!"
        )
        self.gui_root.destroy()

    async def threaded_upload(self, youtube_bulk_upload):
    def threaded_upload(self, youtube_bulk_upload): -> Any
        self.logger.debug("Starting threaded upload")
        try:
            self.gui_root.after(0, lambda: messagebox.showinfo("Success", message))
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            self.logger.error(error_message)
            # Ensure the error message is shown in the GUI as well

    async def select_client_secrets_file(self):
    def select_client_secrets_file(self): -> Any
        self.logger.debug("Selecting client secrets file")
        )
        if filename:
            self.yt_client_secrets_file_var.set(filename)

    async def select_source_directory(self):
    def select_source_directory(self): -> Any
        self.logger.debug("Selecting source directory")
        if directory:
            self.source_directory_var.set(directory)

    async def select_yt_desc_template_file(self):
    def select_yt_desc_template_file(self): -> Any
        self.logger.debug("Selecting YouTube description template file")
        )
        if filename:
            self.yt_desc_template_file_var.set(filename)

    async def clear_log(self):
    def clear_log(self): -> Any
        self.logger.debug("Clearing log output")
        self.log_output.delete("1.0", tk.END)


@dataclass
class ReusableWidgetFrame(tk.LabelFrame):
    async def __init__(self, parent, logger, title, **kwargs):
    def __init__(self, parent, logger, title, **kwargs): -> Any
        self.logger.debug(f"Initializing ReusableWidgetFrame with title: {title}")
        kwargs.setdefault("padx", 10)  # Add default padding on the x-axis
        kwargs.setdefault("pady", 10)  # Add default padding on the y-axis

    async def new_row(self):
    def new_row(self): -> Any
        self.logger.debug("Adding a new row in ReusableWidgetFrame")

    async def add_widgets(self, widgets):
    def add_widgets(self, widgets): -> Any
        self.logger.debug(f"Adding widgets: {widgets}")
        for widget in widgets:

    async def add_find_replace_widgets(self, label_text, summary_tooltip_text):
    def add_find_replace_widgets(self, label_text, summary_tooltip_text): -> Any
        self.logger.debug(f"Adding find/replace widgets with label: {label_text}")

        Tooltip(label, summary_tooltip_text)

        # Listbox with a scrollbar for replacements
        self.replacements_listbox.grid(
        )
        Tooltip(self.replacements_listbox, "Currently active find/replace pairs.")

        # Entry fields for adding new find/replace pairs
        Tooltip(
            find_entry, 
            "Enter text to find. Supports regex syntax for advanced patterns, e.g. [0-9]+ for a sequence of digits.", 
        )
        Tooltip(
            replace_entry, 
            "Enter replacement text. Use regex syntax for advanced patterns, including references to capture strings in the matched text. Leave blank to delete matched text.", 
        )

        # Buttons for adding and removing replacements
        Tooltip(add_button, "Add a new find/replace pair.")
        Tooltip(remove_button, "Remove the selected find/replace pair.")

    async def add_replacement(self):
    def add_replacement(self): -> Any
        self.logger.debug("Adding a replacement")
        if find_text:
            self.replacements_listbox.insert(tk.END, f"{find_text} -> {replace_text}")
            self.find_var.set("")
            self.replace_var.set("")

    async def remove_replacement(self):
    def remove_replacement(self): -> Any
        self.logger.debug("Removing selected replacements")
        for i in reversed(selected_indices):
            self.replacements_listbox.delete(i)

    async def get_replacements(self):
    def get_replacements(self): -> Any
        for item in listbox_items:
            replacements.append((find, replace))
        return replacements


@dataclass
class Tooltip:
    """
    Create a tooltip for a given widget.
    """

    async def __init__(self, widget, text):
    def __init__(self, widget, text): -> Any
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event = None): -> Any
        # Get the widget's location on the screen
        # Adjust the y-coordinate to show the tooltip above the widget or at its top

        # x, y, cx, cy = self.widget.bbox("insert")  # Get widget size
        # x += self.widget.winfo_rootx()
        # y += self.widget.winfo_rooty() + 28

        # Create a toplevel window with required properties
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
            self.tooltip_window, 
        )

    def leave(self, event = None): -> Any
        if self.tooltip_window:
            self.tooltip_window.destroy()


@dataclass
class TextHandler(logging.Handler):
    async def __init__(self, logger, text_widget):
    def __init__(self, logger, text_widget): -> Any
        self.logger.debug("Initializing TextHandler")
        super().__init__()

    async def emit(self, record):
    def emit(self, record): -> Any
        self.text_widget.insert(tk.END, msg + "\\\n")
        self.text_widget.see(tk.END)


@dataclass
class DualLogger:
    """
    A @dataclass
class that can be used to log to both a file and the console at the same time.
    This is used to log to the GUI and to a file at the same time.
    Multiple instances can be used pointing to the same file, and each instance will not overwrite one another.
    """


    async def __init__(self, file_path, stream):
    def __init__(self, file_path, stream): -> Any
        try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.info(f"Failed to open log file {file_path}: {e}")

    async def write(self, message):
    def write(self, message): -> Any
        with self._lock:  # Ensure only one thread can enter this block at a time
            if self.file is not None:
                self.file.write(message)
            if self.stream is not None:
                self.stream.write(message)
            self.flush()  # Ensure the message is written immediately

    async def flush(self):
    def flush(self): -> Any
        if self.file is not None:
            self.file.flush()
        if self.stream is not None:
            self.stream.flush()


async def main():
def main(): -> Any
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # If we're running from a PyInstaller bundle, log to user's home dir
    else:
        # If this GUI was launched from the command line, log to the current directory


    logger.setLevel(logging.DEBUG)


    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    logger.info(
        f"YouTubeBulkUploaderGUI launched, PyInstaller: {running_in_pyinstaller}, Logging to stdout and file: {log_filepath}"
    )

    logger.info("Creating Tkinter GUI root object")

    try:

        logger.debug("Starting main GUI loop")

        logger.info(
            f"If you have encounter any issues with YouTube Bulk Upload, please send Andrew the logs from the file path below!"
        )
        logger.info(f"Log file path: {log_filepath}")

        gui_root.mainloop()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        logger.error(str(e))

        # Pass the error_message variable to the lambda function


if __name__ == "__main__":
    main()
