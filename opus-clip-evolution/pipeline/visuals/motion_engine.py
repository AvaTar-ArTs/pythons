from moviepy import VideoFileClip
import logging

logger = logging.getLogger(__name__)

def apply_motion(video, motion_style="subtle_zoom"):
    """
    Applies motion effects to a clip.
    - subtle_zoom: Slowly zoom in 100% to 105%
    - punch_in: Zoom in to 110%
    - static: No motion
    """
    logger.info(f"Applying motion effect: {motion_style}")
    
    if motion_style == "subtle_zoom":
        # Slowly zoom from 100% to 105% over the duration of the clip
        return video.resized(lambda t: 1 + 0.05 * (t / video.duration))
        
    elif motion_style == "punch_in":
        # Static zoom at 110%
        return video.resized(1.1)
        
    else:
        # Default: no motion
        return video
