class VideoFormatSettings():
    """docstring for ."""

    def __init__(self, arg):
        self.file = {}
        self.allowed_formats = ["MOV","MPEG4","MP4","AVI","WMV","MPEGPS","FLV","3GPP"]

    def file_format(self,format):
        if format in self.allowed_formats:
            self.file["file_format"] = format
