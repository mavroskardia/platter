import os
import cmd


class CommandLineRunner(cmd.Cmd):
    intro = 'REPL for Platter'
    prompt = '> '
    file = None

    def do_test(self, arg):
        print('running tests')

        os.environ['PYSDL2_DLL_PATH'] = 'lib'

    def do_quit(self, arg):
        print('quitting')
        return True

if __name__ == '__main__':

    CommandLineRunner().cmdloop()
