import re
import os
from pathlib import Path

zshrc_path = Path.home() / ".zshrc"

def comment_out_block(content, start_marker_regex, block_name, end_marker_regex=None):
    start_match = re.search(start_marker_regex, content, re.DOTALL)
    if not start_match:
        return content, False # Block not found

    block_start_index = start_match.start()

    if end_marker_regex:
        # Search for the explicit end marker after the start
        end_match = re.search(end_marker_regex, content[block_start_index:], re.DOTALL)
        if end_match:
            block_end_index = block_start_index + end_match.start()
        else:
            block_end_index = len(content) # Fallback to end of file if end marker missing
    else:
        # If no explicit end marker, assume it ends at the start of the next section or EOF
        next_section_start_regex = r'#+\s*[-]+\s*\n#\s*\d+\.\s.*?\n#+\s*[-]+\s*\n'
        next_section_match = re.search(next_section_start_regex, content[block_start_index:], re.DOTALL)
        if next_section_match:
            block_end_index = block_start_index + next_section_match.start()
        else:
            block_end_index = len(content)

    block_content = content[block_start_index:block_end_index]
    
    commented_block = []
    commented_block.append(f"# COMMENT_START: {block_name}")
    for line in block_content.splitlines():
        commented_block.append(f"# {line}")
    commented_block.append(f"# COMMENT_END: {block_name}")

    new_content = content[:block_start_index] + "\n".join(commented_block) + content[block_end_index:]
    return new_content, True


# Read current .zshrc content
current_zshrc_content = zshrc_path.read_text()
original_content_length = len(current_zshrc_content)
changes_made = False

# --- Comment out Section 11: USAGE ANALYTICS (Optimized) ---
section_11_name = "11. USAGE ANALYTICS (Optimized)"
section_11_start_regex = r'#+\s*[-]+\s*\n#\s*11\.\sUSAGE ANALYTICS \(Optimized\)\s*\n#+\s*[-]+\s*\n'
# End of section 11 is the start of section 13
section_11_end_regex = r'#+\s*[-]+\s*\n#\s*13\.\sPROJECT SETUP & PYTHON MANAGEMENT \(Optimized\)\s*\n#+\s*[-]+\s*\n'

modified_content, changed = comment_out_block(current_zshrc_content, section_11_start_regex, section_11_name, end_marker_regex=section_11_end_regex)
if changed:
    current_zshrc_content = modified_content
    changes_made = True
    print(f"✅ Section '{section_11_name}' commented out.")
else:
    print(f"⚠️ Section '{section_11_name}' not found or already modified.")

# --- Comment out the pystatus() function ---
pystatus_name = "pystatus()"
# Look for the pystatus function definition block directly, not just its start line
# Updated regex to match the comment block above the function
pystatus_start_regex = r'(#+\s*[-]+\s*\n#\s*Python environment status\s*\n#+\s*[-]+\s*\n\s*pystatus\(\) {{.*?^\}})'

# We use the generic comment_out_block, but with the specific function pattern as the start_marker
modified_content, changed = comment_out_block(current_zshrc_content, pystatus_start_regex, pystatus_name)
if changed:
    current_zshrc_content = modified_content
    changes_made = True
    print(f"✅ Function '{pystatus_name}' commented out.")
else:
    print(f"⚠️ Function '{pystatus_name}' not found or already modified.")


# Write the modified content back to .zshrc ONLY IF changes occurred
if changes_made:
    zshrc_path.write_text(current_zshrc_content)
    print(f"✅ Updated {zshrc_path} with comments.")
else:
    print(f"No changes applied to {zsh_path}.")