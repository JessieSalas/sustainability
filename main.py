#Main interface loop for Cal Sustainability education platform
import unirest
import time

class ImageRecognizer:
    """
    Recognizes objects in images
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def getApiKey(self):
        """
        Returns the string api key
        """

        return self.api_key
    
    def __imageUpload(self,img,url=False):
        """
        Uploads an image to the camfind api hosted on mashape
        Returns a string token which can be used to retrieve the recognized objects
        
        Parameters
        ----------
        img: file or url
          An image file or url pointing to an image, such as jpeg, to pass to the api

        url: string
          If url is True, the img argument will be interpreted as a url
          instead of a binary image file
        """

        if url == True:
            #configure headers to read an image from an uploaded url
            response = unirest.post("https://camfind.p.mashape.com/image_requests",
              headers={
                "X-Mashape-Key": self.getApiKey(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
              },
              params={
                "image_request[remote_image_url]": img,
                "image_request[altitude]": "27.912109375",
                "image_request[language]": "en",
                "image_request[latitude]": "35.8714220766008",
                "image_request[locale]": "en_US",
                "image_request[longitude]": "14.3583203002251",
              }
            )

        else:
            #configure headers to read an image from local upload
            response = unirest.post("https://camfind.p.mashape.com/image_requests",
              headers={
                "X-Mashape-Key": self.getApiKey(),
              },
              params={
                "image_request[image]": open(img, mode="r"),
                "image_request[altitude]": "27.912109375",
                "image_request[language]": "en",
                "image_request[latitude]": "35.8714220766008",
                "image_request[locale]": "en_US",
                "image_request[longitude]": "14.3583203002251",
              }
            )

        print(response.body)
        return response.body["token"]

    def __getTags(self,token):
        """
        When given a camfind api token, will retrieve the tags associated with the image
        that generated that token
        """
        response = unirest.get("https://camfind.p.mashape.com/image_responses/{0}".format(token),
          headers={
            "X-Mashape-Key": self.getApiKey(),
            "Accept": "application/json"
          }
        )

        #don't need anything else except for body
        response_status = response.body["status"]


        print response.body
        print response_status
        seconds_stalled = 0
        MAX_STALL = 15
        #max stall is the most time you would wait so we don't stall forever
        while (response_status == "not completed") and (seconds_stalled <= MAX_STALL):
            #wait for image recognition to process
            time.sleep(1)
            seconds_stalled += 1
            print("waiting ({0})...".format(seconds_stalled))

            #update response and status 
            response = unirest.get("https://camfind.p.mashape.com/image_responses/{0}".format(token),
              headers={
                "X-Mashape-Key": self.getApiKey(),
                "Accept": "application/json"
              }
            )
            response_status = response.body["status"]
     
        if response_status == "completed":
            tags = response.body["name"]
        else:
            tags = "None"

        return tags


    def recognizeImage(self, img, url=False): 
        """
        Given an image binary file,
        return the central object recognized in the image
        """
        response = self.__getTags(self.__imageUpload(img,url))
        print response
        return response 

if __name__ == "__main__":
    CAMFIND_API_KEY = "Gb6oYTO4HwmshFVDFE2Rnot9Ptdgp1ovy9EjsnKU6flUshv3K8"

    test_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Ursus_arctos_-_Norway.jpg/800px-Ursus_arctos_-_Norway.jpg"
    test_file = "./media/img/bear.jpg"
        
    I = ImageRecognizer(CAMFIND_API_KEY)
    """
    #TESTS
    print("Testing url image recognition")
    I.recognizeImage(test_url, url=True)
    print("Testing uploaded image recognition")
    I.recognizeImage(test_file, url=False)
    """
    #force recognition of already previously uploaded file to save credits
    I.__getTags("mp7gAugjBz2LPbVDa85D5w")

    print("Success!")
