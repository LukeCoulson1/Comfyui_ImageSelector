import torch

class ImageSelector:
    """
    A ComfyUI node that outputs either image1 or image2 based on which one is bypassed.
    If image1 is bypassed (None), it outputs image2.
    If image2 is bypassed (None), it outputs image1.
    If both are provided, it defaults to image1.
    If both are bypassed, it returns a black image.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "fallback_mode": (["image1_priority", "image2_priority"], {
                    "default": "image1_priority"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("output_image",)
    FUNCTION = "select_image"
    CATEGORY = "image/utility"
    
    def select_image(self, image1=None, image2=None, fallback_mode="image1_priority"):
        """
        Select which image to output based on bypass state and fallback mode.
        
        Args:
            image1: First image input (optional)
            image2: Second image input (optional)
            fallback_mode: Which image to prioritize when both are available
        
        Returns:
            The selected image
        """
        
        # Case 1: Only image1 is provided
        if image1 is not None and image2 is None:
            return (image1,)
        
        # Case 2: Only image2 is provided
        if image1 is None and image2 is not None:
            return (image2,)
        
        # Case 3: Both images are provided
        if image1 is not None and image2 is not None:
            if fallback_mode == "image1_priority":
                return (image1,)
            else:  # image2_priority
                return (image2,)
        
        # Case 4: Both are bypassed (None) - create a black fallback image
        # Create a 512x512 black image as fallback
        black_image = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
        return (black_image,)


class ImageSelectorAdvanced:
    """
    An advanced version that provides more control and information about the selection.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "selection_mode": ([
                    "auto_select", 
                    "force_image1", 
                    "force_image2",
                    "image1_priority",
                    "image2_priority"
                ], {
                    "default": "auto_select"
                }),
                "fallback_width": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 2048,
                    "step": 64
                }),
                "fallback_height": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 2048,
                    "step": 64
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("output_image", "selection_info")
    FUNCTION = "select_image_advanced"
    CATEGORY = "image/utility"
    
    def select_image_advanced(self, image1=None, image2=None, selection_mode="auto_select", 
                            fallback_width=512, fallback_height=512):
        """
        Advanced image selection with more control options.
        
        Args:
            image1: First image input (optional)
            image2: Second image input (optional)
            selection_mode: How to select the image
            fallback_width: Width of fallback image when both are bypassed
            fallback_height: Height of fallback image when both are bypassed
        
        Returns:
            Tuple of (selected_image, selection_info_string)
        """
        
        selection_info = ""
        
        # Force modes
        if selection_mode == "force_image1":
            if image1 is not None:
                selection_info = "Forced selection: image1"
                return (image1, selection_info)
            else:
                selection_info = "Forced image1 but bypassed, using fallback"
        elif selection_mode == "force_image2":
            if image2 is not None:
                selection_info = "Forced selection: image2"
                return (image2, selection_info)
            else:
                selection_info = "Forced image2 but bypassed, using fallback"
        
        # Auto selection and priority modes
        elif selection_mode == "auto_select":
            # Auto: use whichever is available, prefer image1 if both
            if image1 is not None and image2 is None:
                selection_info = "Auto selected: image1 (image2 bypassed)"
                return (image1, selection_info)
            elif image1 is None and image2 is not None:
                selection_info = "Auto selected: image2 (image1 bypassed)"
                return (image2, selection_info)
            elif image1 is not None and image2 is not None:
                selection_info = "Auto selected: image1 (both available, image1 priority)"
                return (image1, selection_info)
            else:
                selection_info = "Auto selected: fallback (both bypassed)"
        
        elif selection_mode == "image1_priority":
            if image1 is not None:
                selection_info = "Priority selection: image1"
                return (image1, selection_info)
            elif image2 is not None:
                selection_info = "Priority selection: image2 (image1 bypassed)"
                return (image2, selection_info)
            else:
                selection_info = "Priority selection: fallback (both bypassed)"
        
        elif selection_mode == "image2_priority":
            if image2 is not None:
                selection_info = "Priority selection: image2"
                return (image2, selection_info)
            elif image1 is not None:
                selection_info = "Priority selection: image1 (image2 bypassed)"
                return (image1, selection_info)
            else:
                selection_info = "Priority selection: fallback (both bypassed)"
        
        # Fallback case - create black image
        black_image = torch.zeros((1, fallback_height, fallback_width, 3), dtype=torch.float32)
        return (black_image, selection_info)


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "ImageSelector": ImageSelector,
    "ImageSelectorAdvanced": ImageSelectorAdvanced,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageSelector": "Image Bypasser",
    "ImageSelectorAdvanced": "Image Bypasser (Advanced)",
}