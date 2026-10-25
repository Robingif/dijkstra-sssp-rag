import os
import sys
import argparse
from huggingface_hub import HfApi, create_repo

def deploy(repo_id: str = None, token: str = None):
    """
    Deploys the project directly to Hugging Face Spaces with zero hassle.
    """
    print("=" * 60)
    print("  HUGGING FACE SPACES ONE-CLICK DEPLOYMENT")
    print("=" * 60)

    token = token or os.getenv("HF_TOKEN")
    if not token:
        print("\nNo Hugging Face token detected.")
        print("To deploy:")
        print("  1. Create a free account at: https://huggingface.co/join")
        print("  2. Create a Write token at:   https://huggingface.co/settings/tokens")
        print("     (Click 'Create new token' -> Role: 'Write' -> Copy token)\n")
        try:
            token = input("Please paste your Hugging Face token (starts with hf_...): ").strip()
        except EOFError:
            token = ""

    if not token:
        print("\n❌ Error: Hugging Face token is required to deploy.")
        return

    api = HfApi(token=token)

    try:
        user_info = api.whoami()
        hf_username = user_info.get("name")
        print(f"\n[OK] Authenticated as Hugging Face user: {hf_username}")
    except Exception as e:
        print(f"\n❌ Error: Invalid Hugging Face token or network issue: {e}")
        return

    if not repo_id:
        repo_id = f"{hf_username}/dijkstra-sssp-rag"

    print(f"\n[1/3] Ensuring Space exists at: https://huggingface.co/spaces/{repo_id}...")
    try:
        create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="gradio",
            token=token,
            exist_ok=True
        )
        print("      Space repository ready!")
    except Exception as e:
        print(f"      Space check note: {e}")

    print("\n[2/3] Uploading project files to Hugging Face Space...")
    current_dir = os.path.dirname(os.path.abspath(__file__))

    api.upload_folder(
        folder_path=current_dir,
        repo_id=repo_id,
        repo_type="space",
        ignore_patterns=[
            ".venv/**",
            "__pycache__/**",
            "*.pyc",
            ".git/**",
            "*.bat"
        ]
    )

    print("\n[3/3] Deployment complete!")
    print("=" * 60)
    print(f"🎉 Your interactive app is live at:")
    print(f"    https://huggingface.co/spaces/{repo_id}")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Dijkstra Grounded RAG to Hugging Face Spaces")
    parser.add_argument("--repo", required=False, default=None, help="Your Hugging Face Space ID, e.g., 'username/dijkstra-sssp-rag'")
    parser.add_argument("--token", required=False, default=None, help="Your Hugging Face Write Token (or set HF_TOKEN env var)")
    args = parser.parse_args()
    deploy(args.repo, args.token)
