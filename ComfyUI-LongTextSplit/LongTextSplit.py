import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LongTextSplitterNode:
    def __init__(self):
        self.state_file = os.path.join(os.path.dirname(__file__), "text_splitter_state.json")
        self.state = self.load_state()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_file": ("STRING", {"multiline": False, "default": "Enter the path to your text file here"}),
                "separator": ("STRING", {"default": "---"}),
                "start_index": ("INT", {"default": 0, "min": 0, "max": 10000})
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("prompt", "status", "current_index")
    FUNCTION = "process_text"
    CATEGORY = "LongTextSplit"

    def process_text(self, text_file, separator, start_index):
        try:
            if not text_file.strip() or text_file == "Enter the path to your text file here":
                return ("", "Error: Please provide a valid file path", -1)

            if not os.path.exists(text_file):
                return ("", f"Error: File not found: {text_file}", -1)

            file_changed = self.state.get("last_file") != text_file
            separator_changed = self.state.get("last_separator") != separator
            index_changed = self.state.get("last_start_index") != start_index

            if file_changed or separator_changed:
                self.load_prompts(text_file, separator)
                self.state["last_file"] = text_file
                self.state["last_separator"] = separator
                self.state["current_index"] = start_index
            elif index_changed:
                self.state["current_index"] = start_index
            else:
                self.state["current_index"] = (self.state.get("current_index", 0) + 1) % len(self.state["prompts"])

            self.state["last_start_index"] = start_index
            current_index = self.state["current_index"]

            if current_index < len(self.state["prompts"]):
                prompt = self.state["prompts"][current_index]
            else:
                prompt = ""
                logger.info("No more prompts. Returning empty string.")

            self.save_state()
            
            status = f"Prompt {current_index + 1}/{len(self.state['prompts'])} | File: {os.path.basename(text_file)}"
            return (prompt, status, current_index)
        except Exception as e:
            logger.error(f"Error in process_text: {str(e)}")
            return ("", f"Error: {str(e)}", -1)

    def load_prompts(self, text_file, separator):
        try:
            with open(text_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            self.state["prompts"] = [prompt.strip() for prompt in content.split(separator) if prompt.strip()]
            logger.info(f"Loaded {len(self.state['prompts'])} prompts from {text_file}")
        except Exception as e:
            logger.error(f"Error loading prompts: {str(e)}")
            raise

    def load_state(self):
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading state file: {str(e)}")
        return {"prompts": [], "current_index": 0, "last_file": "", "last_separator": "", "last_start_index": 0}

    def save_state(self):
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f)
        except Exception as e:
            logger.error(f"Error saving state file: {str(e)}")

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

NODE_CLASS_MAPPINGS = {
    "LongTextSplitter": LongTextSplitterNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LongTextSplitter": "Long Text Splitter"
}