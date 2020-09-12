from framework.common import jsonGetter
from pytest_testrail.plugin import pytestrail
from framework.utils import BrowserActions, SystemActions
import pytest
from pajeObjects.pages import loginPage, mainPage
from expressions import post
import time

from framework.logger.logger import Logger
logger = Logger(__file__).getlog()

CONFIG = 'resources/config.json'
TESTDATA = 'resources/testdata.json'

SITE = jsonGetter.GetJson.getFile(CONFIG, "SITE")
API_version = jsonGetter.GetJson.getFile(CONFIG, "API_version")
testdata1 = jsonGetter.GetJson.getFile(TESTDATA, "testdata1")
image_path = jsonGetter.GetJson.getFile(TESTDATA, "image_path")

lp = loginPage.LoginPage
mp = mainPage.MainPage

@pytest.mark.usefixtures("get_driver")
class TestSuite1:
    @pytest.mark.parametrize("login, password, token", testdata1)
    @pytestrail.case('C19380774')
    def test_1(self, login, password, token):
        vkpost = post.Post(token, API_version)
        vkuser = post.User(token, API_version)
        logger.info("Trying to get response")
        BrowserActions.LinkOperations(SITE).get()
        lp().autorize(login, password)
        userid = vkuser.getMyId()
        mp().goToMainPage()

        string = SystemActions.SysOperations.generate_string(16)
        wall_post = vkpost.sendPostToWall(string)
        post_id = wall_post[0]
        post_text = wall_post[1]
        text = mp().findPostTextById(userid, post_id)
        assert string == text, "text not equal to expected: " + string

        newstring = SystemActions.SysOperations.generate_string(16)
        edited = vkpost.editWallPost(userid, post_id, newstring, image_path)
        text1 = mp().findPostTextById(userid, post_id)
        assert newstring == text1, "text not equal to expected: " + string

        result = mp().checkImagePost(post_id)
        assert result != False, "Image has not been attached to wall post"
        dwnld_path = mp().dwnld_path
        compareImage = SystemActions.SysOperations.compare_images(image_path, dwnld_path)
        assert compareImage < 65, "images are different"

        comment_id = vkpost.addComment(post_id, string)
        comment = mp().findComment(comment_id)
        data = [string, str(userid)]
        assert comment == data, "text not as expected"


        mp().clickLikeButton(post_id)
        likes = vkpost.chekPostLikes(post_id)
        assert userid in likes, "Like not founded"
        wall_post1 = mp().findPostById(userid, post_id)
        delete = vkpost.deletePost(post_id)
        time.sleep(1)
        assert mp(wall_post1).isDisplayed() == False, "Post was not deleted"









