from typing import List
import mobase


class MasterOrderChecker(mobase.IPluginDiagnose):
    def __init__(self):
        super(MasterOrderChecker, self).__init__()
        self.__organizer = None

    def init(self, organizer):
        self.__organizer = organizer
        return True

    def requirements(self):
        return []

    def name(self) -> str:
        return "Master Load Order Checker"

    def author(self) -> str:
        return "ForgottenGlory"

    def description(self) -> str:
        return "Checks the load order for out of order masters"

    def version(self) -> mobase.VersionInfo:
        return mobase.VersionInfo(1, 0, 0)

    def isActive(self) -> bool:
        return self.__organizer.pluginSetting(self.name(), "enabled")

    def settings(self) -> List[mobase.PluginSetting]:
        return []

    def shortDescription(self, key: int) -> str:
        return "You have plugins loading before their masters."

    def fullDescription(self, key: int) -> str:
        pluginList = self.__listPlugins()
        pluginListString = "<br><br>•  " + ("<br>•  ".join(pluginList))
        startString = "You have plugins loading before their masters. Manually reorder your plugins to fix this issue. They are:{0}"
        outputString = startString.format(pluginListString)
        outputString += "<br><br>"
        return outputString

    def hasGuidedFix(self, key: int) -> bool:
        return False

    def startGuidedFix(self, key):
        pass

    def __testFile(self, fileName):
        loadingBeforeMaster = False

        # get the priority of the file
        # print(fileName)

        currentPriority = self.__organizer.pluginList().priority(fileName)
        # print(currentPriority)
        if currentPriority == 0:
            return False
        elif currentPriority == -1:
            return False
        elif currentPriority > 0:
            # get the masters of the file
            masters = self.__organizer.pluginList().masters(fileName)
            # print(masters)
            # check if the file has a priority lower than its masters
            for master in masters:
                # print(master + str(self.__organizer.pluginList().priority(master)))
                if currentPriority < self.__organizer.pluginList().priority(master):
                    # print("loading before master!")
                    loadingBeforeMaster = True
                elif (
                    loadingBeforeMaster
                    and currentPriority < self.__organizer.pluginList().priority(master)
                ):
                    loadingBeforeMaster = False

        return loadingBeforeMaster

    def __listPlugins(self):
        for file in self.__listInvalidFiles():
            yield file

    def __listInvalidFiles(self):
        pluginList = self.__organizer.pluginList().pluginNames()
        for name in pluginList:
            if self.__testFile(name):
                yield name

    def __scanPlugins(self):
        return next(self.__listInvalidFiles(), False)

    def activeProblems(self):
        if self.__scanPlugins():
            return [0]
        else:
            return []


def createPlugin() -> mobase.IPluginDiagnose:
    return MasterOrderChecker()
