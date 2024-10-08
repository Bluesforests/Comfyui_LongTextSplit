# Comfyui_LongTextSplit
A concise ComfyUI node, split long text files into multiple prompts, and automatically batch generate images.  

这是一个非常简洁的comfyui节点，主要功能就是将长文本拆分成多条prompt，自动跑图。  
安装方法：把 ComfyUI-LongTextSplit 放到 ComfyUI/custom_nodes/ 目录下，重启 comfyui 即可。  
建议：将节点里的 status 连出来，可以看到拆分提示词的数目，当前在第几条，和一些报错信息。

## Features

- Split long text files into multiple prompts 将长文本分成多条prompt
- Customizable separator for text splitting 可以自定义分隔符
- Automatic state management for continuous processing 可以自动进到下一条prompt，批量跑图

## Installation

1. Navigate to your ComfyUI custom nodes directory:
   ```
   cd /path/to/ComfyUI/custom_nodes/
   ```
2. Clone this repository or download the `ComfyUI-LongTextSplit` folder into the custom nodes directory.
3. Restart ComfyUI or reload the custom nodes.

## Usage

1. In the ComfyUI interface, find the "Long Text Splitter" node under the "ProcessText" category.
2. Connect the node to your workflow.
3. Set the following parameters:
   - `text_file`: Path to your input text file
   - `separator`: The string used to split the text (default is "---")
   - `start_index`: The index of the first segment to start processing (default is 0)
4. Run your workflow. The node will output:
   - `prompt`: The current text segment
   - `status`: Information about the current processing state
   - `current_index`: The index of the current segment
5. Set the batch count for the queue

## Example
[workflow sample](https://github.com/Bluesforests/Comfyui_LongTextSplit/blob/main/ComfyUI-LongTextSplit/workflow-sample.json)   

![image](https://github.com/Bluesforests/Comfyui_LongTextSplit/blob/main/ComfyUI-LongTextSplit/workflow.jpeg)

## Notes

- If you change the input file or separator, the node will reset and start from the beginning of the new text.
- Error messages will be displayed in the `status` output if there are issues with the input file.

## Contributing

Contributions to improve LongTextSplitter are welcome. Please feel free to submit issues or pull requests on the GitHub repository.

## License

[MIT License](https://opensource.org/licenses/MIT)
