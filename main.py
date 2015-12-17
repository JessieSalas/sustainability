#Main interface loop for Cal Sustainability education platform
import unirest
from playvideo import play
import random
import time
import picamera
import pygame
from statement_dict import statements
import pyttsx
#from waste_classifier import *

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

class AudioPlayer:
    """
    Plays audio through standard device output
    """

    def __init__(self):
        print("Initializing audio playback")
        pygame.mixer.init()

    def playAudio(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

class WasteSorter:
    """
    Assigns a label to any String object passed in, one of:
        Compost
        Paper
        Plastic
        Landfill

    """
    def __init__(self):
        print('initialized!')
        self.compost = "Compost"
        self.paper = "Paper"
        self.plastic = "Plastic"
        self.landfill = "Landfill"

    def getBins(self):
        """
        Returns a python list of all bins 
        """
        return [self.compost, self.paper, self.plastic, self.landfill]

    def labelTrash(self, trash):
        """
        Takes in some String trash and outputs a String label, one of:
            Compost
            Paper
            Plastic
            Landfill

        Corresponding to the correct bin it belongs to
        """
        bins = self.getBins()
        #JUNK
        import random
        random.shuffle(bins)
        label = bins[0]

        return label
     
def statement_format(trash):
    """
    Takes in a trash-bin pairing and says something about it
    Trash must be a tuple of length 2
    """
    item = trash[0]
    trashbin = trash[1]
    
    #look up package from statements dictionary 
    package = statements[trashbin]

    bin_statement = package[0]

    facts_list = package[1]

    random.shuffle(facts_list) 
    
    fact = facts_list[0]

    statement = "{0} recognized. That belongs in the {1} bin. Did you know that: {2}".format(item, bin_statement, fact)

    return statement

def sortWrapper(item):
    """
    Wrapper calling sort and talk functions
    """
    correct_bin = waste_sorter(item)
    package = (item, correct_bin)
    s = statement_format(package)
    return s

def poopysort(word): 
    compostable = set([l.lower().strip() for l in open('compostable.txt', 'r')])
    trashable = set([l.lower().strip() for l in open('trash.txt', 'r')])
    paperable = set([l.lower().strip() for l in open('paper.txt', 'r')])
    cansable = set([l.lower().strip() for l in open('cans_bottles.txt', 'r')])
    content = word.split()
    content = [w.lower() for w in content if w.lower() not in ignore] 
    print content
    for c in content:
        if c in compostable: 
            res = 'compost'

        elif c in cansable: 
            res = 'cans'

        elif c in trashable: 
            res = 'trash'

        elif c in paperable: 
            res = 'paper'
        else:
            res = 'trash'

    return res

if __name__ == "__main__":
    camera = picamera.PiCamera()
    camera.capture('capture.jpg')
    ignore = set([l.lower().strip() for l in open('ignore.txt')]) 
    #Initial setup

    
    CAMFIND_API_KEY = "Gb6oYTO4HwmshFVDFE2Rnot9Ptdgp1ovy9EjsnKU6flUshv3K8"

    test_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Ursus_arctos_-_Norway.jpg/800px-Ursus_arctos_-_Norway.jpg"
    #test_file = "./media/img/bear.jpg"
    test_file = 'capture.jpg'

    #initialize image recognition     
    I = ImageRecognizer(CAMFIND_API_KEY)
    im = I.recognizeImage(test_file, url=False)
    ppoop = poopysort(im)
    print ppoop
    play(ppoop)
    #Initialize text to speech
    #I.recognizeImage(test_url, url=True)
    engine = pyttsx.init()
    engine.setProperty('rate', 85)
     
    #Load our trained svm model
    #with open("./waste_sorter_SVM.pickle") as infile:
    #    model = pickle.load(infile)

    #load our Google news 100 billion word context vectors
    #d = toDict("./vectors_100k.txt")

    #while True:
    #    #main interface loop
    #TESTS
    """
    print("Testing url image recognition")
    I.recognizeImage(test_url, url=True)
    print("Testing uploaded image recognition")
    I.recognizeImage(test_file, url=False)
    #force recognition of already previously uploaded file to save credits
    #I._ImageRecognizer__getTags("mp7gAugjBz2LPbVDa85D5w")
    test_audio = "./media/aud/Blip.wav"
    P = AudioPlayer()
    P.playAudio(test_audio)
    #W = WasteSorter()
    #print(W.labelTrash("banana"))
    """
    print("Success!")
