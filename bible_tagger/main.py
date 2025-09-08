import click
from bible_tagger import bible_api, storage

@click.group()
def cli():
    """A CLI for tagging Bible verses."""
    pass

@cli.command()
@click.argument("reference")
@click.argument("tags", nargs=-1)
def tag(reference, tags):
    """Tag a Bible verse with one or more tags."""
    if not tags:
        click.echo("Please provide at least one tag.")
        return

    try:
        verse_reference, verse_text = bible_api.get_verse(reference)
        storage.add_verse(verse_reference, verse_text, list(tags))
        click.echo(f"Tagged '{verse_reference}' with: {', '.join(tags)}")
    except bible_api.VerseNotFoundException as e:
        click.echo(str(e))

@cli.command()
@click.argument("tag_name")
def show(tag_name):
    """Show all verses tagged with a specific tag."""
    verses = storage.get_verses_by_tag(tag_name)
    if not verses:
        click.echo(f"No verses found with tag: {tag_name}")
        return

    for verse in verses:
        click.echo(f"{verse['reference']}: {verse['text']}")
        click.echo(f"  Tags: {', '.join(verse['tags'])}")
        click.echo()

@cli.command()
def tags():
    """List all tags."""
    all_tags = storage.get_all_tags()
    if not all_tags:
        click.echo("No tags found.")
        return

    for tag in all_tags:
        click.echo(tag)

if __name__ == "__main__":
    cli()
