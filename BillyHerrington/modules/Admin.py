from modules import Updater
from modules import Delete
import constants


def update():
    answer = Updater.update()
    return answer


def delete():
    answer = Delete.delete()
    return answer


modes = {constants.ADMIN_UPDATE_preview: constants.ADMIN_UPDATE, constants.ADMIN_DELETE_preview: constants.ADMIN_DELETE,
         constants.ADMIN_MANAGEPERMISSIONS_preview: constants.ADMIN_MANAGEPERMISSIONS,
         constants.ADMIN_GETLOGS_preview: constants.ADMIN_GETLOGS, constants.ADMIN_CLEARLOGS_preview: constants.ADMIN_CLEARLOGS,
         constants.ADMIN_STOPBILLY_preview: constants.ADMIN_STOPBILLY}
