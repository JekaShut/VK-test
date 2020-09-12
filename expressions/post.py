from framework.utils import APIUtils
from VKAPI import VKAPI


class Post:
    def __init__(self, token, API_version):
        self.vkapi = VKAPI.VkApiUtils(token, API_version)
        self.image_path = 'resources\\files\\img.jpg'
        self.responce = 'response'
        self.postId = 'post_id'
        self.id = 'id'
        self.message = 'message'
        self.comment_id = 'comment_id'
        self.items = 'items'

    def sendPostToWall(self, string):
        response = self.vkapi.wallPost(string)
        post = response.get(self.responce)
        id = post.get(self.postId)
        text = post.get(self.message)
        return id, text

    def postImageToWall(self, user_id, image_path = ""):
        image = self.vkapi.uploadImage(user_id, self.image_path)
        result = self.vkapi.wallPostImage(image)
        return result

    def editWallPost(self, user_id, post_id, post_text = "", image_path = ""):
        image = self.vkapi.uploadImage(user_id, self.image_path)
        post = self.vkapi.wallEdit(post_id, post_text, image)
        return post

    def addComment(self, post_id, text):
        result = self.vkapi.wallComment(post_id, text)
        responce = result.get(self.responce)
        id = responce.get(self.comment_id)
        return id

    def deletePost(self, post_id):
        result = self.vkapi.wallDelete(post_id)
        return result

    def chekPostLikes(self, post_id):
        result = self.vkapi.getPostLikes(post_id)
        responce = result.get(self.responce)
        id = responce.get(self.items)
        return id

class User:
    def __init__(self, token, API_version):
        self.vkapi = VKAPI.VkApiUtils(token, API_version)
        self.responce = 'response'
        self.id = 'id'

    def getMyId(self):
        response = self.vkapi.usersGet()
        user_id = response.get(self.responce)
        user_id = user_id[0]
        id = user_id.get(self.id)
        return id