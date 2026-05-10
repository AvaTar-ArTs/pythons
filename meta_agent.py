
import argparse
import subprocess
import json

def run_refactoring(repo_path, prompt_path, strategy):
    """
    Executes the user's refactoring tool.

    NOTE: This is a placeholder. You'll need to replace the command
    with the actual command to run your refactoring tool.
    """
    print(f"Running refactoring strategy '{strategy}'...")

    # --- ACTION REQUIRED ---
    # Replace this with the actual command to run your tool.
    # For example:
    #
    # command = [
    #     "your_script_name",
    #     "--repo-path", repo_path,
    #     "--prompt-path", prompt_path,
    #     "--strategy", strategy
    # ]
    #
    command = [
        "echo",
        "This is a placeholder for your refactoring tool."
    ]
    # ---------------------

    try:
        subprocess.run(command, check=True, text=True, capture_output=True)
        print("Refactoring completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during refactoring: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: The command '{command[0]}' was not found.")
        print("Please make sure your script is in your PATH or provide the full path.")
        return False


def analyze_refactoring(repo_path):
    """
    Analyzes the results of the refactoring using git-ai.

    This function assumes that the refactoring process creates one or more
    commits, and that git-ai is tracking the prompts and changes.
    """
    print("Analyzing refactoring results with git-ai...")

    # For simplicity, we'll analyze the last commit.
    # A more advanced version could analyze a range of commits.
    try:
        get_last_commit_sha = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "HEAD"],
            check=True, text=True, capture_output=True
        )
        commit_sha = get_last_commit_sha.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting last commit SHA: {e}")
        return None

    print(f"Analyzing commit: {commit_sha}")

    # Use git-ai to get the acceptance rate for the prompts in the last commit
    query = f"""
    SELECT
        AVG(accepted_rate) as avg_acceptance_rate,
        COUNT(*) as prompt_count
    FROM prompts
    WHERE commit_sha = '{commit_sha}'
    """

    try:
        # Initialize the prompts database for the given repository
        subprocess.run(
            ["git-ai", "--repo-path", repo_path, "prompts"],
            check=True, text=True, capture_output=True
        )

        # Execute the query
        result = subprocess.run(
            ["git-ai", "--repo-path", repo_path, "prompts", "exec", query, "--json"],
            check=True, text=True, capture_output=True
        )
        analysis_data = json.loads(result.stdout)
        return analysis_data[0] if analysis_data else None
    except subprocess.CalledProcessError as e:
        print(f"Error analyzing refactoring with git-ai: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error parsing git-ai output: {e}")
        return None


def generate_report(analysis_results):
    """
    Generates a report based on the analysis.
    """
    if not analysis_results:
        print("Could not generate a report: no analysis data.")
        return

    print("
--- Refactoring Analysis Report ---")
    prompt_count = analysis_results.get("prompt_count", 0)
    avg_rate = analysis_results.get("avg_acceptance_rate")

    if prompt_count == 0:
        print("No prompts were found for the last commit.")
        print("Make sure git-ai is tracking your AI-assisted commits.")
        return

    print(f"Number of prompts analyzed: {prompt_count}")
    if avg_rate is not None:
        print(f"Average acceptance rate: {avg_rate:.2%}")
        if avg_rate < 0.5:
            print("Suggestion: The acceptance rate is low. Consider refining your prompts.")
            print("You could try providing more context or more specific examples.")
        else:
            print("Suggestion: The acceptance rate is good. Keep up the great work!")
    print("---------------------------------")


def main():
    parser = argparse.ArgumentParser(
        description="A meta-agent to orchestrate refactoring and analysis."
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="The path to the git repository to refactor."
    )
    parser.add_argument(
        "--prompt-path",
        required=True,
        help="The path to the directory containing your refactoring prompts."
    )
    parser.add_argument(
        "--strategy",
        default="refactor",
        help="The refactoring strategy to use."
    )
    args = parser.parse_args()

    # Phase 1: Refactor
    if not run_refactoring(args.repo_path, args.prompt_path, args.strategy):
        print("Aborting due to refactoring failure.")
        return

    # Phase 2: Analyze
    analysis_results = analyze_refactoring(args.repo_path)

    # Phase 3: Report
    generate_report(analysis_results)


if __name__ == "__main__":
    main()
