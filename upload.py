import cloudinary
import cloudinary.uploader
import cloudinary.api


def cloudUpload(localfile):
    """
    takes localfile stored on disk and returns a url to which it is uploaded
    using cloudinary api
    """
    
    cloudinary.config( cloud_name = "dkljngqnl", api_key = "495869372656521", api_secret = "trdnXjXXQVo9LDdpawK0b8W0s7c" )

    b = cloudinary.uploader.upload(localfile)

    hosted_url = b["secure_url"]
    return hosted_url

