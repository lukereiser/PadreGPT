#!/usr/bin/env python3
"""
Add new files to the existing Padre GPT Assistant.
Uses file_search tool resources to attach files directly.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PDF_DIR = Path(__file__).parent.parent / "downloads" / "telegram_pdfs" / "2025-12"

# Files to upload (smaller ones first, skip very large files)
FILES_TO_UPLOAD = [
    # Original priority files (smaller)
    "Theology for Beginners - Frank Sheed.pdf",
    "A Catechism of Christian Doctrine - Ireland 1951.pdf",
    "Thomas Aquinas_ Contra Errores Graecorum_ English.pdf",
    "How_to_Study_being_The_Letter_of_St_Thomas_Aquinas_to_Brother_John.pdf",
    "The Practice Of Humility - Pope Leo XIII.pdf",
    "Uniformity with God's Will - St. Alphonsus de Ligouri.pdf",
    "St. Justin Martyr-The First Apology of Justin.pdf",
    "St. Justin Martyr-2nd Apology.pdf",
    "The_First_Seven_Ecumenical_Councils_325_787_Their_History_and_Theology.pdf",
    # New downloads
    "Catechism_of_the_Catholic_Church_2000.pdf",  # 14MB
    "Douay_Rheims_Bible_Complete.txt",  # 5.6MB text
    # Large files - skip Summa (37MB) and Encyclicals (27MB) as they timeout
]


def upload_file(path: Path) -> str:
    """Upload a single file and return its ID."""
    with open(path, "rb") as f:
        file = client.files.create(file=f, purpose="assistants")
    return file.id


def main():
    print("=" * 60)
    print("🙏 ADDING FILES TO PADRE GPT")
    print("=" * 60)
    
    assistant_id = os.getenv("ASSISTANT_ID") or os.getenv("OPENAI_ASSISTANT_ID")
    if not assistant_id:
        print("❌ ASSISTANT_ID not found in .env")
        sys.exit(1)
    
    print(f"\n📋 Assistant ID: {assistant_id}")
    
    # Upload files
    print("\n📤 UPLOADING FILES")
    print("-" * 40)
    
    file_ids = []
    for filename in FILES_TO_UPLOAD:
        path = PDF_DIR / filename
        if not path.exists():
            print(f"⚠️  Not found: {filename}")
            continue
        
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f"📤 {filename} ({size_mb:.1f}MB)...", end=" ", flush=True)
        try:
            file_id = upload_file(path)
            file_ids.append(file_id)
            print(f"✅")
        except Exception as e:
            print(f"❌ {e}")
    
    print(f"\n📁 Uploaded {len(file_ids)} files")
    
    # Update assistant with file_search using file_ids
    print("\n🤖 UPDATING ASSISTANT")
    print("-" * 40)
    
    try:
        # Update assistant to use file_search with these files
        assistant = client.beta.assistants.update(
            assistant_id,
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {
                    "vector_stores": [{
                        "file_ids": file_ids
                    }]
                }
            }
        )
        print(f"✅ Assistant updated!")
    except Exception as e:
        print(f"❌ Error updating assistant: {e}")
        print("\n💡 Trying alternate approach - creating assistant with files...")
        
        # Create new assistant with files
        assistant = client.beta.assistants.create(
            name="Padre GPT v2",
            instructions="""You are Padre GPT, a Catholic theologian with deep expertise in Catholic theology, particularly the works of St. Thomas Aquinas.

Your role is to:
1. Answer questions from an authentically Catholic perspective, grounded in Catholic theology
2. Draw from the uploaded documents including Church Fathers, Catechisms, Papal documents, and theological texts
3. Provide accurate, respectful, and thoughtful responses
4. Emphasize the works and thoughts of Thomas Aquinas when relevant
5. Cite sources from the uploaded documents when possible

You should:
- Be charitable and patient in explanations
- Distinguish between dogma, doctrine, and theological opinion
- Encourage deeper study of the faith
- Point users to relevant Church documents and teachings""",
            model="gpt-4o",
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {
                    "vector_stores": [{
                        "file_ids": file_ids
                    }]
                }
            }
        )
        
        print(f"✅ New assistant created: {assistant.id}")
        
        # Update .env with new assistant ID
        env_path = PDF_DIR.parent.parent / ".env"
        with open(env_path, "r") as f:
            content = f.read()
        
        if "ASSISTANT_ID=" in content:
            lines = content.split("\n")
            new_lines = []
            for line in lines:
                if line.startswith("ASSISTANT_ID="):
                    new_lines.append(f"ASSISTANT_ID={assistant.id}")
                else:
                    new_lines.append(line)
            content = "\n".join(new_lines)
        else:
            content += f"\nASSISTANT_ID={assistant.id}\n"
        
        with open(env_path, "w") as f:
            f.write(content)
        
        print(f"💾 Updated .env with new ASSISTANT_ID")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ SUCCESS!")
    print("=" * 60)
    print(f"\n📁 Total files uploaded: {len(file_ids)}")
    print("\n📚 Knowledge base includes:")
    for f in FILES_TO_UPLOAD:
        if (PDF_DIR / f).exists():
            print(f"   ✅ {f}")
    
    print("\n🚀 Run 'streamlit run app.py' to test!")


if __name__ == "__main__":
    main()
