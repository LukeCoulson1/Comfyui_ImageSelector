# ComfyUI Image Selector

![GitHub](https://img.shields.io/github/license/LukeCoulson1/Comfyui_ImageSelector)
![GitHub stars](https://img.shields.io/github/stars/LukeCoulson1/Comfyui_ImageSelector)
![GitHub issues](https://img.shields.io/github/issues/LukeCoulson1/Comfyui_ImageSelector)

A custom ComfyUI node that intelligently selects between two image inputs based on which ones are bypassed (disconnected). Perfect for conditional image processing workflows.

## Features

### Basic Image Selector
- **Smart Selection**: Automatically outputs the available image when one input is bypassed
- **Fallback Handling**: Provides a black fallback image when both inputs are bypassed
- **Priority Control**: Choose which image to prefer when both are connected

### Advanced Image Selector
- **Multiple Selection Modes**: Auto-select, force selection, or priority-based selection
- **Selection Information**: Outputs a text string explaining which image was selected and why
- **Custom Fallback Size**: Configure the dimensions of the fallback image
- **Detailed Control**: More granular control over selection behavior

## Installation

### Method 1: ComfyUI Manager (Recommended)
1. Install [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)
2. Open ComfyUI and go to Manager → Install Custom Nodes
3. Search for "Image Selector" or "Snowshoes311"
4. Click Install and restart ComfyUI

### Method 2: Git Clone
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/LukeCoulson1/Comfyui_ImageSelector.git
```

### Method 3: Manual Download
1. Download this repository as a ZIP file
2. Extract the `comfyui_image_selector` folder to your ComfyUI custom nodes directory:
   ```
   ComfyUI/custom_nodes/comfyui_image_selector/
   ```

3. Restart ComfyUI or refresh the node list

3. The nodes will appear in the `image/utility` category

## Node Types

### Image Selector (Basic)

**Inputs:**
- `image1` (IMAGE, optional): First image input
- `image2` (IMAGE, optional): Second image input  
- `fallback_mode` (dropdown): Choose priority when both images are available
  - `image1_priority`: Prefer image1 (default)
  - `image2_priority`: Prefer image2

**Outputs:**
- `output_image` (IMAGE): The selected image

**Behavior:**
- If only `image1` is connected → outputs `image1`
- If only `image2` is connected → outputs `image2`
- If both are connected → outputs based on `fallback_mode`
- If neither is connected → outputs a 512x512 black image

### Image Selector (Advanced)

**Inputs:**
- `image1` (IMAGE, optional): First image input
- `image2` (IMAGE, optional): Second image input
- `selection_mode` (dropdown): How to select the image
  - `auto_select`: Smart selection based on availability
  - `force_image1`: Always try to use image1
  - `force_image2`: Always try to use image2
  - `image1_priority`: Prefer image1 when both available
  - `image2_priority`: Prefer image2 when both available
- `fallback_width` (INT): Width of fallback image (64-2048, default: 512)
- `fallback_height` (INT): Height of fallback image (64-2048, default: 512)

**Outputs:**
- `output_image` (IMAGE): The selected image
- `selection_info` (STRING): Text description of what was selected

## Usage Examples

### Basic Conditional Processing
```
[Image Generator 1] → [Image Selector] → [Final Output]
[Image Generator 2] ↗
```
When you bypass (disconnect) Image Generator 1, the selector automatically switches to Image Generator 2.

### A/B Testing Pipeline
```
[Style A] → [Image Selector Advanced] → [Preview]
[Style B] ↗
```
Use the advanced node with `selection_info` output to see which style is currently active.

### Fallback Safety Net
```
[Primary Process] → [Image Selector] → [Always Has Output]
[Backup Process] ↗
```
Ensures your workflow always produces an image, even if the primary process fails or is bypassed.

## Technical Details

- **Image Format**: Standard ComfyUI IMAGE format (torch tensors)
- **Bypass Detection**: Uses Python `None` check to detect bypassed inputs
- **Memory Efficient**: Only processes the selected image
- **Thread Safe**: Can be used in parallel workflows

## Common Use Cases

1. **Conditional Generation**: Switch between different generation methods
2. **A/B Comparisons**: Easy switching between processing variants  
3. **Fallback Systems**: Ensure workflows always produce output
4. **Dynamic Pipelines**: Runtime selection based on upstream conditions
5. **Debug Workflows**: Easily switch inputs during development

## Troubleshooting

**Node doesn't appear**: Check that files are in the correct custom_nodes directory and restart ComfyUI

**Black output when expecting image**: Both inputs may be bypassed - check your connections

**Wrong image selected**: Verify your selection mode and priority settings

## License

This node is provided as-is for ComfyUI workflows. Feel free to modify and distribute.

## Contributing

To add features or report issues:
1. Test thoroughly with different bypass combinations
2. Ensure backward compatibility with existing workflows
3. Update documentation for any new features