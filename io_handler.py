
class IOHandler():
    def __init__(self, legal_actions):
        self.legal_actions = legal_actions

    def print_help_menu(self):
        print('Action\tDescription')
        for key, val in self.legal_actions.items():
            print(f'  {key}\t{val[0]}')

    def get_user_input(self):
        while True:
            print('Pick an action')
            action = input('> ').upper()
            try:
                return self.legal_actions[action]
            except Exception as e:
                print(f"Error: {e} is not a valid action key.")
                print(f"Possible keys: {list(self.legal_actions.keys())}")