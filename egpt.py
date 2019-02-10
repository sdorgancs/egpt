import click
import egpt.processing as proc
import prettyprinter # type: ignore
from distributed import Client # type: ignore
prettyprinter.install_extras(
    # Comment out any packages you are not using.
    include=[
        'dataclasses',
    ],
    warn_on_error=True
)

@click.group()
def jobgroup():
    pass


@jobgroup.group("job")
def job():
    pass

@job.command("run")
@click.argument("jobfile")
@click.option("--scheduler")
def run(jobfile:str, scheduler:str):
    if scheduler is not None:
        Client(scheduler)
    else:
        Client()
    proc.submit(jobfile)

cli = click.CommandCollection(sources=[jobgroup])

if __name__ == '__main__':
    cli()
