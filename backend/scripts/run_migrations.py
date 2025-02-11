"""Script to run migrations for both production and test databases."""
import os
import subprocess
import click


@click.command()
@click.option('--env', type=click.Choice(['prod', 'test', 'both']), default='both', help='Target environment')
@click.option('--action', type=click.Choice(['upgrade', 'downgrade']), default='upgrade', help='Migration action')
@click.option('--revision', default='head', help='Target revision (default: head)')
def run_migrations(env: str, action: str, revision: str):
    """Run database migrations for the specified environment."""
    
    def execute_migration(is_test: bool):
        env_vars = os.environ.copy()
        if is_test:
            env_vars["USE_TEST_DB"] = "true"
            print("\nRunning migrations for TEST database...")
        else:
            env_vars["USE_TEST_DB"] = ""
            print("\nRunning migrations for PRODUCTION database...")
        
        try:
            subprocess.run(
                ["alembic", action, revision],
                env=env_vars,
                check=True
            )
            print("Migration completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error running migration: {e}")
            raise click.Abort()

    if env in ['prod', 'both']:
        execute_migration(False)
    
    if env in ['test', 'both']:
        execute_migration(True)


if __name__ == '__main__':
    run_migrations()
