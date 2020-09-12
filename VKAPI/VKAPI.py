#from framework.Base.BaseElement import *
import requests
from framework.logger.logger import Logger
from framework.common import jsonGetter


logger = Logger(__file__).getlog()

tokenKey = 'access_token'
messageKey = 'message'
attachments = 'attachments'
server = 'server'
hash = 'hash'
type = 'type'
post = 'post'
versionKey = 'v'
ID = 'id'
item_id = 'item_id'
user_id = 'user_id'
owner_id = 'owner_id'
photo = 'photo'
responce = 'response'
post_id = 'post_id'
uploadUrl = 'upload_url'

CONFIG = 'resources/config.json'
APIHost = jsonGetter.GetJson.getFile(CONFIG, "APIHost")

class VkApiUtils:
    def __init__(self, token, api_vesrion):
        self.token = token
        self.version = api_vesrion
        self.wallPost = "method/wall.post"
        self.usersGet = "method/users.get"
        self.wallImageServer = "method/photos.getWallUploadServer"
        self.saveWallPhoto = "method/photos.saveWallPhoto"
        self.wallEdit = "method/wall.edit"
        self.wallComment = "method/wall.createComment"
        self.wallDelete = "method/wall.delete"
        self.getLikes = "method/likes.getList"

    def usersGet(self):
        logger.info("Trying to get user id")
        user_id = requests.post(APIHost + self.usersGet, data={tokenKey: self.token,
                                                                versionKey: self.version}).json()
        return user_id

    def uploadImage(self, user_id, image_path):
        logger.info("Trying to upload an image")
        response = requests.post(APIHost + self.wallImageServer, data={tokenKey: self.token,
                                                                    versionKey: self.version}).json()
        link = response.get(responce)
        url = link.get(uploadUrl)
        response1 = requests.post(url, files={photo: open(image_path, "rb")}).json()
        response2 = requests.post(APIHost + self.saveWallPhoto, data={tokenKey: self.token,
                                                                        user_id: str(user_id),
                                                                        photo: response1.get(photo),
                                                                        server: response1.get(server),
                                                                        hash: response1.get(hash),
                                                                        versionKey: self.version}).json()
        response2 = response2.get(responce)[0]
        image = photo + str(response2[owner_id]) + '_' + str(response2[ID])
        return image

    def wallPost(self, message="no message given"):
        logger.info("Trying to send post to wall with message: "+ message)
        text = requests.post(APIHost + self.wallPost, data={tokenKey: self.token,
                                                                    messageKey: message,
                                                                    versionKey: self.version}).json()
        return text

    def wallPostImage(self, image):
        logger.info("Trying to post an image")

        response3 = requests.post(APIHost + self.wallPost, data={tokenKey: self.token,
                                                                   attachments: image,
                                                                    versionKey: self.version}).json()

        return response3

    def wallEdit(self, post_id, post_text= "", image= ""):
        logger.info("Trying to edit wall post")
        response = requests.post(APIHost + self.wallEdit, data ={tokenKey: self.token,
                                                                   post_id: post_id,
                                                                   attachments: image,
                                                                    messageKey: post_text,
                                                                    versionKey: self.version}).json()
        return response

    def wallDelete(self, post_id):
        logger.info("Trying to delete wall post")
        response = requests.post(APIHost + self.wallDelete, data={tokenKey: self.token,
                                                                     post_id: post_id,
                                                                     versionKey: self.version}).json()
        return response

    def getPostLikes(self, post_id):
        logger.info("Trying to get all likes on wall post")
        response = requests.post(APIHost + self.getLikes, data={tokenKey: self.token,
                                                                  type: post,
                                                                    item_id: post_id,
                                                                    versionKey: self.version}).json()
        return response

    def wallComment(self, post_id, text):
        logger.info("Trying to leve a comment for post: " + str(post_id))
        response = requests.post(APIHost + self.wallComment, data={tokenKey: self.token,
                                                                  post_id: post_id,
                                                                  messageKey: text,
                                                                  versionKey: self.version}).json()
        return response