import config
import constants


def getVersion():
    return config.version


def getAuthor():
    return "Created by Serabobina."


modes = {constants.ABOUT_GETVERSION_preview: constants.ABOUT_GETVERSION,
         constants.ABOUT_AUTHOR_preview: constants.ABOUT_AUTHOR}
