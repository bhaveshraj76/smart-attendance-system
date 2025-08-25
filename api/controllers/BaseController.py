from config.Constants import constants
from config.Messages import messages
from utils.TimesheetUtil import timesheetHelperUtil

class BaseController:
    def __init__(self):
        self.constants = constants
        self.messages = messages
        self.timesheetHelperUtil = timesheetHelperUtil



