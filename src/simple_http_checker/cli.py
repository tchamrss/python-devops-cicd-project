import logging
import click
from .checker import check_urls

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] - %(levelname)-8s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("urls", nargs=-1)
@click.option("--timeout", default=5, help="Timeout for the HTTP request in seconds.")
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging.")
def main(urls, timeout, verbose):
    """A simple HTTP checker that checks the status of a list of URLs."""

    if verbose:
        logger.debug(
            f"Received Verbose mode is on {verbose}. Setting log level to DEBUG."
        )
        logger.setLevel(logging.DEBUG)
    else:
        logger.info("Verbose mode is off. Use --verbose or -v to enable debug logging.")

    if not urls:
        logger.error("No URLs provided. Please provide at least one URL to check.")
        click.echo(
            "usage: check-urls <URL> [<URL> ...] [--timeout <seconds>] [--verbose]"
        )
        return
    else:
        logger.debug(f"Received {urls} URLs to check.")

    logger.info(
        f"Starting HTTP checker for {len(urls)} URLs with a timeout of {timeout} seconds."
    )

    results = check_urls(urls, timeout)

    click.echo("\n--- Results ---")

    for url, status in results.items():
        if "OK" in status:
            click.secho(f"{url:<40} --> {status}", fg="green")
        else:
            click.secho(f"{url:<40} --> {status}", fg="red")

        # click.echo(f"{url:<40} --> {status}")
        # logger.info(f"{url:<40} --> {status}")
