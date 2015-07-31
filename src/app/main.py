if __name__ == '__main__':
    import sys
    import os

    os.environ['PYSDL2_DLL_PATH'] = os.path.abspath('lib')

    try:
        import sdl2
    except Exception as e:
        sys.stderr.write('You must have pysdl2 installed to run this game. '
                         '(pip install pysdl2)')
        sys.stderr.write('\n\n{}\n\n'.format(str(e)))
        sys.exit(1)

    from .app import App

    print('Running app.')

    retcode = App().run()

    print('App finished with exit code {}.'.format(retcode))

    sys.exit(retcode)
