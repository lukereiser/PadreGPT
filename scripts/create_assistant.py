#!/usr/bin/env python3
"""
Create a Padre GPT Assistant using OpenAI's Assistants API.
Uploads PDFs and creates an assistant with file search capability.
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuration
PDF_DIR = Path(__file__).parent.parent / "downloads" / "telegram_pdfs" / "2025-12"
ASSISTANT_NAME = "Padre GPT"
ASSISTANT_INSTRUCTIONS = """You are Padre GPT, a faithful Catholic theologian and teacher. Your mission is to help people understand the Catholic faith by drawing from the authentic sources of Catholic teaching.

## CRITICAL: SOURCE PRIORITY (Always follow this order)

When answering questions, you MUST search your uploaded documents and cite sources in this priority:

### 1. 📖 HOLY SCRIPTURE (Highest Authority)
- Always start with relevant Scripture passages from the Douay-Rheims Bible
- Quote the exact text with book, chapter, and verse
- Example: "As Our Lord teaches: 'I am the way, and the truth, and the life. No man cometh to the Father, but by me.' (John 14:6)"

### 2. 📜 THE CATECHISM (Official Church Teaching)
- Quote from the Catechism of the Catholic Church with paragraph numbers
- Example: "The Catechism teaches: '...' (CCC 1234)"

### 3. ⛪ CHURCH FATHERS & DOCTORS (Authoritative Witnesses)
- Quote St. Thomas Aquinas, St. Augustine, St. Justin Martyr, etc.
- Include the work name and relevant section
- Example: "St. Thomas Aquinas explains in the Summa Theologica (I, Q.2, A.3): '...'"

### 4. 📚 PAPAL DOCUMENTS & COUNCILS (Magisterial Teaching)
- Quote encyclicals, council documents, papal writings
- Include document name and section if possible

## RESPONSE FORMAT

For every theological question:

1. **Search your documents first** - Always use file_search to find relevant passages
2. **Begin with Scripture** if applicable
3. **Quote directly** - Use exact quotes with citations, not paraphrases
4. **Explain clearly** - After quoting, explain what the source teaches
5. **Connect sources** - Show how Scripture, Catechism, and Fathers agree

## EXAMPLE RESPONSE FORMAT

**Question**: "What does the Church teach about the Real Presence?"

**Good Response**:
> The Church's teaching on the Real Presence is firmly grounded in Scripture and Tradition.
>
> **Sacred Scripture** teaches us through Our Lord's own words:
> "This is my body, which is given for you" (Luke 22:19)
> "Except you eat the flesh of the Son of man, and drink his blood, you shall not have life in you." (John 6:54)
>
> **The Catechism** affirms: "In the most blessed sacrament of the Eucharist 'the body and blood, together with the soul and divinity, of our Lord Jesus Christ and, therefore, the whole Christ is truly, really, and substantially contained.'" (CCC 1374)
>
> **St. Thomas Aquinas** explains the mode of this presence in the Summa Theologica...

## CONDUCT GUIDELINES

**You should:**
- Be charitable, patient, and encouraging
- Distinguish between dogma (must believe), doctrine (Church teaching), and theological opinion
- Encourage deeper study and prayer
- Recommend the user speak with a priest for pastoral guidance when appropriate
- Use traditional Catholic terminology (e.g., "Holy Mass" not just "Mass")

**You must NOT:**
- Give personal opinions that contradict Church teaching
- Present theological speculation as defined doctrine
- Be dismissive of sincere questions, even difficult ones
- Recommend sources outside your uploaded documents without noting they're external

## WHEN YOU DON'T KNOW

If a question is outside your uploaded sources:
- Say "I don't find specific teaching on this in my sources"
- Suggest the user consult a priest or the Vatican website
- Never invent citations or make up quotes

Remember: You represent authentic Catholic teaching. Every answer should help the faithful grow closer to Christ through His Church.
"""

# Priority files - Essential Catholic texts
PRIORITY_FILES = [
    # Core Theology
    "Theology for Beginners - Frank Sheed.pdf",
    "A Catechism of Christian Doctrine - Ireland 1951.pdf",
    "Catechism_of_the_Catholic_Church.pdf",  # Modern CCC
    "Reason_Informed_by_Faith_Foundations_of_Catholic_Morality_Richard.pdf",  # Moral theology
    "Denzinger_Sources_of_Catholic_Dogma.pdf",  # THE definitive collection of Church teachings
    "Mere_Christianity_CS_Lewis.pdf",  # C.S. Lewis apologetics classic
    
    # Thomas Aquinas & Summa
    "Thomas Aquinas_ Contra Errores Graecorum_ English.pdf",
    "How_to_Study_being_The_Letter_of_St_Thomas_Aquinas_to_Brother_John.pdf",
    "Saint Thomas and the Greeks - Anton Charles Pegis.pdf",  # Thomistic philosophy
    "Summa_Theologica_Part1_Prima_Pars.txt",
    "Summa_Theologica_Part1-2_Prima_Secundae.txt",
    "Summa_Theologica_Part2-2_Secunda_Secundae_Vol1.txt",
    "Summa_Theologica_Part3_Tertia_Pars.txt",
    
    # Sacred Scripture
    "Douay_Rheims_Bible_Complete.txt",
    
    # Church Fathers & Early Church
    "St. Justin Martyr-The First Apology of Justin.pdf",
    "St. Justin Martyr-2nd Apology.pdf",
    "The_First_Seven_Ecumenical_Councils_325_787_Their_History_and_Theology.pdf",
    
    # St. Augustine
    "City_of_God_Volume_I_Augustine.txt",
    "City_of_God_Volume_II_Augustine.txt",
    "Confessions_Augustine.txt",
    
    # Mystical & Spiritual Classics
    "Imitation_of_Christ_Thomas_a_Kempis.txt",
    "The_little_garden_of_roses_and_valley_of_lilies_Thomas_a_Kempis.pdf",  # More Kempis
    "The_Mystical_Doctrine_of_St_John_of_the_Cross_R_H_J_Steuart;_John.pdf",  # Doctor of the Church
    "The way of interior peace - Edouard de Lehen.pdf",  # Spiritual classic
    "Edith-Stein - Selected-Writings.pdf",  # St. Teresa Benedicta of the Cross
    
    # Liturgy & Sacraments
    "Pastoral-Liturgy - Josef-a-Jungmann.pdf",  # Foremost liturgy scholar
    "Sin_and_Confession_on_the_Eve_of_the_Reformation_Thomas_N_Tentler.pdf",  # Confession
    "Saint-LEONARD-of-Puerto-Mauricio-Method-to-Hear-Mass.pdf",  # The Holy Mass
    "Directory_on_popular_piety_and_liturgy_principles_and_guidelines.pdf",  # Vatican document
    
    # Ecclesiology & Apologetics
    "The_primacy_of_the_apostolic_see,_vindicated_Kenrick,_Francis_Patrick.pdf",  # Papal primacy
    "Enchiridion_of_Commonplaces,_against_Luther_and_Enemies_of_the_Church.pdf",  # Apologetics
    
    # Marian Devotion
    "Maximilian-Kolbe-s-Consecration-to-Mary.pdf",  # St. Maximilian Kolbe
    
    # Papal & Spiritual
    "The Practice Of Humility - Pope Leo XIII.pdf",
    "Uniformity with God's Will - St. Alphonsus de Ligouri.pdf",
    "The papal encyclicals  1958-1981.pdf",
]


def get_files_to_upload(priority_only=True):
    """Get list of files to upload (PDFs and TXTs)."""
    if priority_only:
        files = []
        for name in PRIORITY_FILES:
            path = PDF_DIR / name
            if path.exists():
                files.append(path)
            else:
                print(f"⚠️  Not found: {name}")
        return files
    else:
        pdfs = list(PDF_DIR.glob("*.pdf"))
        txts = list(PDF_DIR.glob("*.txt"))
        return pdfs + txts


def upload_files(file_paths):
    """Upload files (PDF and TXT) to OpenAI."""
    uploaded_file_ids = []
    
    for file_path in file_paths:
        print(f"📤 Uploading: {file_path.name}...", end=" ", flush=True)
        try:
            with open(file_path, "rb") as f:
                file = client.files.create(file=f, purpose="assistants")
            uploaded_file_ids.append(file.id)
            print(f"✅ ({file.id})")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return uploaded_file_ids


def create_assistant(file_ids):
    """Create the Padre GPT assistant with retrieval."""
    print("\n🤖 Creating assistant...", end=" ", flush=True)
    
    # Create assistant with file_search tool
    # Files will be attached to threads when chatting
    assistant = client.beta.assistants.create(
        name=ASSISTANT_NAME,
        instructions=ASSISTANT_INSTRUCTIONS,
        model="gpt-4o",
        tools=[{"type": "file_search"}],
    )
    
    print(f"✅ ({assistant.id})")
    return assistant, file_ids


def main():
    print("=" * 60)
    print("🙏 PADRE GPT ASSISTANT CREATOR")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in .env")
        sys.exit(1)
    
    # Get files to upload
    print(f"\n📁 Looking for files in: {PDF_DIR}")
    files_to_upload = get_files_to_upload(priority_only=True)
    print(f"📚 Found {len(files_to_upload)} priority files\n")
    
    if not files_to_upload:
        print("❌ No files found!")
        sys.exit(1)
    
    # Upload files
    print("📤 UPLOADING FILES")
    print("-" * 40)
    file_ids = upload_files(files_to_upload)
    
    if not file_ids:
        print("❌ No files uploaded!")
        sys.exit(1)
    
    # Create assistant
    assistant, file_ids = create_assistant(file_ids)
    
    # Save assistant ID and file IDs
    print("\n" + "=" * 60)
    print("✅ PADRE GPT ASSISTANT CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n📋 Assistant ID: {assistant.id}")
    print(f"📁 File IDs: {len(file_ids)} files uploaded")
    
    # Append to .env
    env_path = Path(__file__).parent.parent / ".env"
    with open(env_path, "a") as f:
        f.write(f"\n# Padre GPT Assistant\n")
        f.write(f"ASSISTANT_ID={assistant.id}\n")
        f.write(f"FILE_IDS={','.join(file_ids)}\n")
    
    print(f"\n💾 IDs saved to .env")
    print("\n🚀 Next: Run 'streamlit run app.py' to start the web interface!")


if __name__ == "__main__":
    main()
