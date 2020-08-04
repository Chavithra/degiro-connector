
import click
import os

# pylint: disable=no-value-for-parameter

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')

class MyCLI(click.MultiCommand):
    """ This class is loading commands from the "plugin_folder". """
    
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.startswith('__'):
                continue
            elif filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + '.py')
        with open(fn) as f:
            content = f.read()
            if len(content) > 0:
                code = compile(content, fn, 'exec')
                eval(code, ns, ns)
                return ns['cli']

cli = MyCLI(
    help= """
    This tool\'s will take a quotecast feed from Degiro\'s API.\n
    """
)

if __name__ == '__main__':
    cli()