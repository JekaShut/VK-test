from framework.utils import ElementOperations
from framework.Base.BaseElement import By, Keys
from framework.Base.BaseForm import BaseForm
import re

class MainPage(BaseForm):
    def __init__(self, elem = ""):
        BaseForm.__init__(self, elem)
        self.mainPageButton = ElementOperations.Button(By.XPATH, "//li[@id='l_pr']/a")
        self.firstPostText = ElementOperations.Label(By.XPATH, "//div[@class='wall_post_cont _wall_post_cont']")
        self.id = "id"
        self.idPrefix = "wpt"
        self.partContainsDivClass = '//a[contains(@onclick, "'
        self.closeAfterVar = '") and contains(@title, "Нравится")]'
        self.commentTextStart = '//div[contains(@id, "'
        self.commentTextEnd = '")]/div[@class="wall_reply_text"]'
        self.parent = '//parent::div'
        self.imagePathStart = '//div[contains(@id, "'
        self.imagePathEnd = '") and @class = "wall_post_cont _wall_post_cont"]/div[@class="page_post_sized_thumbs  clear_fix"]/a'
        self.pattern = r"\d+"
        self.back = "/.."
        self.dwnld_path = 'resources/files/filename.png'




    def goToMainPage(self):
        self.mainPageButton.click()

    def getFirstPost(self):
        text = self.firstPostText.getText()
        id = self.firstPostText.getAttr(self.id)
        return text, id

    def findPostById(self, user_id, post_id):
        id = self.idPrefix + str(user_id) + "_" + str(post_id)
        elem = ElementOperations.Button(By.ID, id)._find()
        return elem

    def findPostTextById(self, user_id, post_id):
        id = self.idPrefix + str(user_id) + "_" + str(post_id)
        text = ElementOperations.Label(By.ID, id).getText()
        return text

    def clickLikeButton(self, post_id):
        path = self.partContainsDivClass + str(post_id) + self.closeAfterVar
        ElementOperations.Button(By.XPATH, path).click()

    def findComment(self, comment_id):
        path = self.commentTextStart + str(comment_id) + self.commentTextEnd
        text = ElementOperations.Label(By.XPATH, path).getText()
        user = path + self.back
        string = ElementOperations.Label(By.XPATH, user).getAttr(self.id)
        id = re.findall(self.pattern, string)[0]
        return [text, id]

    def checkImagePost(self, post_id):
        path = self.imagePathStart + str(post_id) + self.imagePathEnd
        elem = ElementOperations.Button(By.XPATH, path)
        elem.move()
        elem.send(Keys.DOWN)
        image = elem._find(5)
        with open(self.dwnld_path, 'wb') as file:
            file.write(image.screenshot_as_png)
        return image

