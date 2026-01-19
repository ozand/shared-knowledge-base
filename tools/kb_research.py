#!/usr/bin/env python3
"""
Research Assistant Tool
Helper for the Research Agent to manage raw data and synthesis.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import re

class ResearchManager:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.cache_dir = repo_root / ".kb" / "cache" / "research"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def start_session(self, topic: str):
        """Initialize a research session folder."""
        slug = re.sub(r'[^a-z0-9-]', '-', topic.lower()).strip('-')
        session_dir = self.cache_dir / slug
        session_dir.mkdir(exist_ok=True)
        
        # Create manifest
        manifest_path = session_dir / "manifest.json"
        if not manifest_path.exists():
            manifest = {
                "topic": topic,
                "started_at": datetime.now().isoformat(),
                "status": "in_progress",
                "sources": []
            }
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
        
        print(f"✅ Research session started: {session_dir}")
        print(f"   Topic: {topic}")
        return session_dir

    def save_snippet(self, topic: str, source_url: str, content: str, title: str = "Snippet"):
        """Save a research snippet."""
        slug = re.sub(r'[^a-z0-9-]', '-', topic.lower()).strip('-')
        session_dir = self.cache_dir / slug
        
        if not session_dir.exists():
            print(f"❌ Session not found for topic: {topic}. Run 'start' first.")
            return

        # Generate filename
        timestamp = datetime.now().strftime("%H%M%S")
        safe_title = re.sub(r'[^a-z0-9-]', '-', title.lower()).strip('-')[:30]
        filename = f"{timestamp}_{safe_title}.md"
        file_path = session_dir / filename

        # Write content with frontmatter
        full_content = f"""---
source_url: {source_url}
captured_at: {datetime.now().isoformat()}
---

# {title}

{content}
"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)

        # Update manifest
        manifest_path = session_dir / "manifest.json"
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        manifest["sources"].append({
            "file": filename,
            "url": source_url,
            "title": title
        })
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"✅ Saved snippet: {file_path}")

    def list_sessions(self):
        """List active research sessions."""
        if not self.cache_dir.exists():
            print("No research sessions found.")
            return

        print("\n📂 Research Sessions:")
        for d in self.cache_dir.iterdir():
            if d.is_dir() and (d / "manifest.json").exists():
                print(f"  - {d.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KB Research Tool")
    subparsers = parser.add_subparsers(dest="command")

    start_parser = subparsers.add_parser("start", help="Start a research session")
    start_parser.add_argument("topic", help="Topic to research")

    save_parser = subparsers.add_parser("save", help="Save a research snippet")
    save_parser.add_argument("topic", help="Session topic")
    save_parser.add_argument("url", help="Source URL")
    save_parser.add_argument("content", help="Content to save")
    save_parser.add_argument("--title", default="Snippet", help="Title of the snippet")

    list_parser = subparsers.add_parser("list", help="List sessions")

    args = parser.parse_args()
    
    manager = ResearchManager(Path.cwd())

    if args.command == "start":
        manager.start_session(args.topic)
    elif args.command == "save":
        manager.save_snippet(args.topic, args.url, args.content, args.title)
    elif args.command == "list":
        manager.list_sessions()
    else:
        parser.print_help()
