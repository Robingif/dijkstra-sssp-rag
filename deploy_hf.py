import os
import argparse
from huggingface_hub import HfApi, create_repo

def deploy(repo_id: str, token: str = None):
    """
    Deploys the current project directly to Hugging Face Spaces in one click.
    """
    token = token or os.getenv("HF_TOKEN")
    if not token:
        print("Error: Hugging Face API token is required.")
        print("Set HF_TOKEN environment variable or pass --token <your_token>.")
        return

    api = HfApi(token=token)
    
    print(f"Ensuring Space exists: {repo_id}...")
    try:
        create_repo(repo_id=repo_id, repo_type="space", space_sdk="gradio", token=token, exist_ok=True)
        print(f"Space verified: https://huggingface.co/spaces/{repo_id}")
    except Exception as e:
        print(f"Note on repo creation: {e}")

    print("Uploading project files to Hugging Face Space...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    api.upload_folder(
        folder_path=current_dir,
        repo_id=repo_id,
        repo_type="space",
        ignore_patterns=[".venv/**", "__pycache__/**", "*.pyc", ".git/**"]
    )
    print("\n✅ Deployment complete!")
    print(f"Your interactive app is live at: https://huggingface.co/spaces/{repo_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Dijkstra Grounded RAG to Hugging Face Spaces")
    parser.add_argument("--repo", required=True, help="Your Hugging Face Space ID, e.g., 'username/dijkstra-sssp-rag'")
    parser.add_argument("--token", required=False, help="Your Hugging Face Write Token (or set HF_TOKEN env var)")
    args = parser.parse_args()
    deploy(args.repo, args.token)
