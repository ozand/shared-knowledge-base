#!/usr/bin/env python
"""
SKU CLI - Shared Knowledge Utility
Main entry point for CLI commands
"""

import click
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from catalog import CatalogManager
from sync import SyncManager
from install import InstallManager
from publish import PublishManager
from auth import AuthManager
from utils import console, error, success, warning

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Shared Knowledge Utility (sku) - Enterprise Knowledge Graph for Claude Code"""
    pass

@cli.group()
def auth():
    """Authentication commands"""
    pass

@auth.command()
@click.option('--token', help='GitHub personal access token')
def login(token):
    """Authenticate with GitHub"""
    auth_mgr = AuthManager()
    auth_mgr.login(token)
    success("✓ Authenticated successfully")

@auth.command()
def logout():
    """Logout and clear credentials"""
    auth_mgr = AuthManager()
    auth_mgr.logout()
    success("✓ Logged out successfully")

@cli.command()
@click.option('--index-only', is_flag=True, help='Sync catalog index only (fast, ~5KB)')
@click.option('--category', help='Sync specific category')
@click.option('--all', 'sync_all', is_flag=True, help='Sync all artifacts (slow)')
@click.option('--force', is_flag=True, help='Force re-download even if cached')
def sync(index_only, category, sync_all, force):
    """Sync artifacts from shared-knowledge-base"""
    sync_mgr = SyncManager()

    if index_only:
        console.print("[dim]Syncing catalog index only...[/dim]")
        sync_mgr.sync_index(force)
        success("✓ Catalog synced")
        console.print(f"  Total artifacts: {sync_mgr.get_artifact_count()}")

    elif category:
        console.print(f"[dim]Syncing category: {category}[/dim]")
        sync_mgr.sync_category(category, force)
        success(f"✓ Category '{category}' synced")

    elif sync_all:
        warning("Syncing all artifacts may take a while...")
        if click.confirm("Continue?"):
            sync_mgr.sync_all(force)
            success("✓ All artifacts synced")
        else:
            console.print("Cancelled")

    else:
        console.print("[dim]Syncing installed artifacts...[/dim]")
        sync_mgr.sync_installed(force)
        success("✓ Installed artifacts synced")

@cli.command()
@click.option('--type', 'artifact_type', help='Filter by artifact type')
@click.option('--category', help='Filter by category')
@click.option('--tag', help='Filter by tag')
@click.option('--project', help='Filter by project')
@click.option('--search', help='Search in name/description')
def list(artifact_type, category, tag, project, search):
    """List available artifacts"""
    catalog = CatalogManager()
    artifacts = catalog.list_artifacts(
        type=artifact_type,
        category=category,
        tag=tag,
        project=project,
        search=search
    )

    from rich.table import Table
    from rich.console import Console as RichConsole
    rich_console = RichConsole()

    table = Table(title=f"Available Artifacts")
    table.add_column("Type", style="cyan", width=10)
    table.add_column("ID", style="green", width=25)
    table.add_column("Name", style="white", width=30)
    table.add_column("Version", style="yellow", width=10)
    table.add_column("Size", style="dim", width=10)
    table.add_column("Project", style="blue", width=15)

    for artifact in artifacts:
        table.add_row(
            artifact.get('type', 'N/A'),
            artifact.get('id', 'N/A')[:25],
            artifact.get('name', 'N/A')[:30],
            artifact.get('version', 'N/A'),
            f"{artifact.get('size_kb', 0)} KB",
            artifact.get('project', 'shared')
        )

    rich_console.print(table)
    console.print(f"\nTotal: {len(artifacts)} artifacts")

@cli.command()
@click.argument('query')
def search(query):
    """Search artifacts by query"""
    catalog = CatalogManager()
    artifacts = catalog.search(query)

    from rich.table import Table
    from rich.console import Console as RichConsole
    rich_console = RichConsole()

    table = Table(title=f"Search Results: '{query}'")
    table.add_column("Type", style="cyan")
    table.add_column("ID", style="green")
    table.add_column("Name", style="white")
    table.add_column("Description", style="dim")

    for artifact in artifacts:
        table.add_row(
            artifact.get('type', 'N/A'),
            artifact.get('id', 'N/A'),
            artifact.get('name', 'N/A'),
            artifact.get('description', 'N/A')[:50]
        )

    rich_console.print(table)
    console.print(f"\nFound: {len(artifacts)} artifacts")

@cli.command()
@click.argument('artifact_type')
@click.argument('artifact_id')
def info(artifact_type, artifact_id):
    """Show detailed information about an artifact"""
    catalog = CatalogManager()
    artifact = catalog.get_artifact(artifact_type, artifact_id)

    if not artifact:
        error(f"Artifact not found: {artifact_type}/{artifact_id}")
        sys.exit(1)

    # Display artifact info
    console.print(f"\n[bold cyan]{artifact.get('type', 'N/A').upper()}[/bold cyan]: {artifact.get('id')}")
    console.print(f"[bold white]{artifact.get('name')}[/bold white]")
    console.print(f"Version: [yellow]{artifact.get('version')}[/yellow]")
    console.print(f"Size: [dim]{artifact.get('size_kb', 0)} KB[/dim]")

    if artifact.get('description'):
        console.print(f"\nDescription:\n  {artifact['description']}")

    if artifact.get('tags'):
        console.print(f"\nTags: {', '.join(artifact['tags'])}")

    if artifact.get('dependencies'):
        console.print(f"\nDependencies:")
        for dep in artifact['dependencies']:
            console.print(f"  • {dep}")

    console.print(f"\nPath: [dim]{artifact.get('path')}[/dim]")

@cli.command()
@click.argument('artifact_type')
@click.argument('artifact_id')
@click.option('--force', is_flag=True, help='Overwrite if exists')
def install(artifact_type, artifact_id, force):
    """Install artifact from shared-knowledge-base"""
    install_mgr = InstallManager()

    console.print(f"[dim]Installing {artifact_type}/{artifact_id}...[/dim]")

    # Check if artifact exists
    catalog = CatalogManager()
    artifact = catalog.get_artifact(artifact_type, artifact_id)

    if not artifact:
        error(f"Artifact not found: {artifact_type}/{artifact_id}")
        sys.exit(1)

    # Install
    try:
        install_mgr.install(artifact, force)
        success(f"✓ Installed {artifact_type}/{artifact_id}")

        # Show what was installed
        console.print(f"  Version: {artifact.get('version')}")
        console.print(f"  Location: {install_mgr.get_install_path(artifact)}")

        # Check dependencies
        if artifact.get('dependencies'):
            console.print("\n[dim]Installing dependencies...[/dim]")
            for dep in artifact['dependencies']:
                console.print(f"  • {dep}")
                # TODO: install dependencies

    except Exception as e:
        error(f"✗ Installation failed: {e}")
        sys.exit(1)

@cli.command()
@click.argument('artifact_type')
@click.argument('artifact_id')
def uninstall(artifact_type, artifact_id):
    """Remove installed artifact"""
    install_mgr = InstallManager()
    install_mgr.uninstall(artifact_type, artifact_id)
    success(f"✓ Uninstalled {artifact_type}/{artifact_id}")

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--type', 'artifact_type', required=True, help='Artifact type (mcp|docs|config|schema)')
@click.option('--version', required=True, help='Artifact version (semver)')
@click.option('--name', help='Artifact name')
@click.option('--tags', help='Comma-separated tags')
@click.option('--description', help='Artifact description')
def publish(path, artifact_type, version, name, tags, description):
    """Publish project artifact to shared-knowledge-base"""
    publish_mgr = PublishManager()

    console.print(f"[dim]Publishing {artifact_type} artifact...[/dim]")

    try:
        artifact_id = publish_mgr.publish(
            path=path,
            artifact_type=artifact_type,
            version=version,
            name=name,
            tags=tags,
            description=description
        )

        success(f"✓ Published {artifact_type}/{artifact_id}")
        console.print(f"  Version: {version}")
        console.print(f"  Path: {path}")

        # Remind to commit
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("  1. Review changes in shared-knowledge-base")
        console.print("  2. Update catalog/index.yaml if needed")
        console.print("  3. Commit and push changes:")
        console.print("     git add .")
        console.print("     git commit -m 'Publish {artifact_type}/{artifact_id}'")
        console.print("     git push")

    except Exception as e:
        error(f"✗ Publish failed: {e}")
        sys.exit(1)

@cli.command()
@click.option('--type', help='Update specific type')
@click.option('--artifact', 'artifact_id', help='Update specific artifact')
@click.option('--all', 'update_all', is_flag=True, help='Update all installed')
def update(type, artifact_id, update_all):
    """Update installed artifacts"""
    # TODO: Implement update logic
    if update_all:
        console.print("[dim]Checking for updates...[/dim]")
        # Check all installed artifacts
        # Update if newer version available
    elif type and artifact_id:
        console.print(f"[dim]Updating {type}/{artifact_id}...[/dim]")
        # Update specific artifact
    else:
        console.print("[dim]Checking for updates...[/dim]")
        # Just check, don't update

@cli.command()
def check_updates():
    """Check if updates are available for installed artifacts"""
    # TODO: Implement check updates logic
    console.print("[dim]Checking for updates...[/dim]")
    # Compare installed versions with catalog
    # Show available updates

@cli.command()
def status():
    """Show installation status and cache info"""
    from rich.panel import Panel
    from rich.console import Console as RichConsole
    rich_console = RichConsole()

    catalog = CatalogManager()
    install_mgr = InstallManager()

    # Catalog status
    catalog_info = catalog.get_status()
    rich_console.print(Panel(
        f"Version: {catalog_info.get('version')}\n"
        f"Last Updated: {catalog_info.get('last_updated')}\n"
        f"Total Artifacts: {catalog_info.get('total_artifacts')}",
        title="📚 Catalog Status",
        border_style="blue"
    ))

    # Installed artifacts
    installed = install_mgr.list_installed()
    if installed:
        from rich.table import Table
        table = Table(title="Installed Artifacts")
        table.add_column("Type", style="cyan")
        table.add_column("ID", style="green")
        table.add_column("Version", style="yellow")

        for item in installed:
            table.add_row(
                item['type'],
                item['id'],
                item['version']
            )

        rich_console.print(table)
    else:
        console.print("\n[dim]No artifacts installed yet[/dim]")

def main():
    """Main entry point"""
    cli()

if __name__ == "__main__":
    main()
