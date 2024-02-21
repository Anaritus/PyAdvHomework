import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('file', type=click.File('r'), default='-')
def nl(file=None):
    counter = 1
    while True:
        row = file.readline()
        if not row:
            break
        click.echo(f'{counter: 6}  {row.strip()}')
        counter += 1


def tailSingle(file):
    rows = []
    row = ''
    for t in file.read():
        if t == '\n':
            rows.append(row)
            row = ''
        else:
            row += t
    last = -16 if file.isatty() else -9
    return '\n'.join(rows[last::])


class filesDefaultStdin(click.Argument):
    def __init__(self, *args, **kwargs):
        kwargs['nargs'] = -1
        kwargs['type'] = click.File('r')
        super().__init__(*args, **kwargs)

    def process_value(self, ctx, value):
        return super().process_value(ctx, value or ('-',))


@cli.command()
@click.argument('files', cls=filesDefaultStdin)
def tail(files):
    if len(files) == 1:
        click.echo(tailSingle(files[0]))
        return
    for file in files:
        click.echo(f'==> {file.name} <==')
        click.echo(tailSingle(file))


def wcSingle(file):
    lines = file.readlines()
    return (
        len(lines),
        sum(len(line.split()) for line in lines),
        sum(len(line.encode()) for line in lines),
    )


def wcFormat(nl, w, c, file_name):
    click.echo(f'{nl: 8}{w: 8}{c: 8} {file_name}')


@cli.command()
@click.argument('files', cls=filesDefaultStdin)
def wc(files):
    totalLines, totalWords, totalChrs = 0, 0, 0
    for file in files:
        newlines, words, chrs = wcSingle(file)
        totalLines += newlines
        totalWords += words
        totalChrs += chrs
        name = file.name if not file.isatty() else ''
        wcFormat(newlines, words, chrs, name)
    if len(files) > 1:
        wcFormat(totalLines, totalWords, totalChrs, 'total')


if __name__ == '__main__':
    cli()
