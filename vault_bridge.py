import frontmatter
from pathlib import Path

class ObsidianVaultBridge:
    """
    A utility class to bridge Python automation with Obsidian knowledge vaults.
    Allows automated scripts to update note frontmatter or content.
    """
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)

    def update_note_frontmatter(self, note_path: str, new_data: dict):
        """
        Updates the YAML frontmatter of a given note in the vault.
        """
        full_path = self.vault_path / note_path
        if not full_path.exists():
            print(f"Error: Note {full_path} not found.")
            return

        with open(full_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        post.metadata.update(new_data)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

# Usage Example:
# bridge = ObsidianVaultBridge("/Users/steven/Guides")
# bridge.update_note_frontmatter("10 Projects/Project_Inventory.md", {"updated_at": "2026-05-19"})
