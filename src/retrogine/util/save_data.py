from typing import Dict

class Saver:
    def __init__(self, file_name):
        self.__file_name = file_name
    
    def save_to_json(self, content: Dict) -> None:
        pass

    def check_data_exist(self) -> None:
        pass

if __name__ == "__main__":
      save = Saver()
