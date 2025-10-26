class Invoker():

    def __init__(self):
        self.__executed = []
        self.__undone = []

    def execute_command(self, command):
        command.execute()
        self.__executed.append(command)

    def undo_last(self):
        if self.__executed:
            command = self.__executed.pop()
            command.undo()
            self.__undone.append(command)

    def redo_last(self):
        if self.__undone:
            command = self.__undone.pop()
            command.execute()
            self.__executed.append(command)

