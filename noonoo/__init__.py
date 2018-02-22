import click
from lib import ECR


@click.command()
@click.argument('repository')
@click.option('--region', help='The AWS region of the ECR')
@click.option('--remove_untagged', is_flag=True, help='Remove all images without tags')
@click.option('--keep', default=50, help='How many old images to keep')
@click.option('--prompt', default=False, is_flag=True, help='Prompt before deleting')
@click.option('-n', '--dryrun', default=False, is_flag=True, help='Only print intentions')
def janitor(repository, region, remove_untagged, keep, prompt, dryrun):
    """ Clean up older/untagged images from an ECR.  """
    ecr = ECR(region=region)
    images = sorted(
        ecr.list_images(repository),
        key=lambda x: x.pushed_at,
        reverse=True
    )
    to_delete = []
    to_keep = keep

    click.echo("Found {} images in ECR, will keep {}".format(len(images), keep))
    if prompt and not click.confirm("Continue?"):
        return

    for image in images:
        if remove_untagged:
            if image.tags is None:
                to_delete.append(image)
                continue

        if to_keep == 0:
            to_delete.append(image)
            continue

        to_keep -= 1
        click.echo("keeping: {}".format(image))

    click.echo("Deleting: {}".format(len(to_delete)))
    if prompt:
        if not click.confirm("Images slated for deletion: {}".format(to_delete)):
            return

    if not dryrun:
        ecr.delete_images(repository, to_delete)
        click.echo(u"Done, deleted")


if __name__ == "__main__":
    janitor()
