import sys

class CheckEnv:

    def in_venv(self):
        return (hasattr(sys, 'real_prefix') or
                (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

    def check(self):
        if not self.in_venv():
            print("Looks like not in virtual environment.. please activate it")
            exit()
        else:
            print("in venv")
