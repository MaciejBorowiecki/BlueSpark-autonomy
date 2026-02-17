class RemoteVisionAddonsError(Exception):
    """Base Error class"""
    pass

class CameraError(RemoteVisionAddonsError):
    """Camera error"""
    pass

class StreamError(RemoteVisionAddonsError):
    """Preview streming error"""
    pass