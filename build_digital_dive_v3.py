import os

HUB_ROOT = "/Users/steven/DiGiTaLDiVe"

# --- THE "EMPIRE v3" MAP (Intelligence & Assets) ---
symlinks = {
    # Intelligence & Nervous System
    "5_Command_Reports/Nervous_System_APIs": "/Users/steven/.env.d",
    "1_Active_Revenue/Swarm_Orchestration": "/Users/steven/SWARM_V3_NATIVE_HANDOFF.md",
    
    # Visual Assets
    "2_Passive_Income/Visual_Product_Library/Pixel_Hearts": "/Users/steven/Pictures/pixel-hearts",
    "2_Passive_Income/Visual_Product_Library/DaLLe_Archive": "/Users/steven/Pictures/DaLLe",
    
    # Narrative AI Engine
    "3_Intellectual_Property/Narrative_AI_Engine": "/Users/steven/Music/nocTurneMeLoDieS/python",
}

def execute_v3():
    print(f"\n🚀 EXECUTING DiGiTaLDiVe v3 UPGRADE...")
    for logical_path, physical_path in symlinks.items():
        full_dest_path = os.path.join(HUB_ROOT, logical_path)
        dest_dir = os.path.dirname(full_dest_path)
        if not os.path.exists(dest_dir): os.makedirs(dest_dir)
        if not os.path.exists(full_dest_path):
            try:
                os.symlink(physical_path, full_dest_path)
                print(f"  ✅ Linked: {os.path.basename(full_dest_path)}")
            except Exception as e: print(f"  ❌ Error: {e}")
    print("\n✨ v3 UPGRADE COMPLETE.")

if __name__ == "__main__":
    execute_v3()
