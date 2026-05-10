import click
from .quantum_media_processor import QuantumMediaProcessor
from .chaos_scheduler import ChaosScheduler


@click.group()
def cli():
    """QuantumForge CLI - Where Order Meets Chaos"""
    pass


@click.argument("output_path")
def process_image(chaos, input_path, output_path):
    """Quantum-inspired image processing"""
    qmp = QuantumMediaProcessor(chaos_factor=chaos)
    scheduler = ChaosScheduler()
    try:
        scheduler.schedule_operation(
            lambda: qmp.process_image(input_path, output_path), criticality=2
        )
        click.echo(f"Processed {input_path} → {output_path}")
    except RuntimeError as e:
        click.secho(f"Chaos failure: {e}", fg="red")


if __name__ == "__main__":
    cli()
