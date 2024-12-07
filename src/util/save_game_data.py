class SaveGame:
    def __init__(self):
        pass

    def save_game_data(self) -> None:
        pass

    def check_file_exists(self) -> bool:
        pass

    def test_run(self):
        print('Saving is running. . . .')

if __name__ == "__main__":
      save = SaveGame()
      save.test_run()