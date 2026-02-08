#!/usr/bin/env env python3
"""
Extract the base character vocabulary from GPT-1's BPE tokenizer.

This script downloads the GPT-1 tokenizer files (if needed) and extracts
the 478 base characters that form the foundation of the BPE vocabulary.
"""

import os
import json
import urllib.request
from pathlib import Path

# Use system temp directory for downloads
TEMP_DIR = Path("/tmp/gpt1_tokenizer")
TEMP_DIR.mkdir(exist_ok=True)

# GPT-1 (openai-gpt) tokenizer files from Hugging Face
VOCAB_URL = "https://huggingface.co/openai-gpt/resolve/main/vocab.json"
MERGES_URL = "https://huggingface.co/openai-gpt/resolve/main/merges.txt"

VOCAB_FILE = TEMP_DIR / "vocab.json"
MERGES_FILE = TEMP_DIR / "merges.txt"


def download_file(url, dest):
    """Download a file if it doesn't exist."""
    if dest.exists():
        print(f"✓ Found existing file: {dest}")
        return

    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, dest)
    print(f"✓ Downloaded to {dest}")


def extract_base_characters():
    """Extract base characters from GPT-1 tokenizer."""
    # Download tokenizer files
    download_file(VOCAB_URL, VOCAB_FILE)
    download_file(MERGES_URL, MERGES_FILE)

    # Load vocabulary
    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        vocab = json.load(f)

    # Load merges to understand what's a base character vs merged token
    with open(MERGES_FILE, 'r', encoding='utf-8') as f:
        merges = [line.strip() for line in f if line.strip()]

    print(f"\n📊 Tokenizer Statistics:")
    print(f"Total vocabulary size: {len(vocab)}")
    print(f"Number of BPE merges: {len(merges)}")

    # Base characters are tokens that don't appear as results of merges
    # In BPE, merged tokens are combinations of existing tokens
    merged_tokens = set()
    for merge in merges:
        parts = merge.split()
        if len(parts) == 2:
            # The result of merging is the concatenation
            merged_token = ''.join(parts)
            merged_tokens.add(merged_token)

    # Base characters are tokens NOT created by merges
    base_chars = []
    for token, idx in sorted(vocab.items(), key=lambda x: x[1]):
        if token not in merged_tokens:
            base_chars.append(token)

    print(f"Number of base characters: {len(base_chars)}")

    # Display the base characters
    print(f"\n📝 Base Characters ({len(base_chars)} total):")
    print("=" * 80)

    # Group by category for readability
    ascii_printable = []
    whitespace = []
    special = []
    unicode_chars = []

    for char in base_chars:
        if len(char) == 1:
            code = ord(char)
            if 32 <= code <= 126:  # ASCII printable
                ascii_printable.append(char)
            elif char in [' ', '\t', '\n', '\r']:
                whitespace.append(char)
            elif code < 128:
                special.append(char)
            else:
                unicode_chars.append(char)
        else:
            # Multi-character tokens in base vocab (shouldn't happen but check)
            special.append(char)

    if ascii_printable:
        print(f"\nASCII Printable ({len(ascii_printable)}):")
        print(''.join(ascii_printable))

    if whitespace:
        print(f"\nWhitespace ({len(whitespace)}):")
        for char in whitespace:
            print(f"  {repr(char)}")

    if special:
        print(f"\nSpecial/Control Characters ({len(special)}):")
        for char in special[:50]:  # Limit output
            print(f"  {repr(char)}")
        if len(special) > 50:
            print(f"  ... and {len(special) - 50} more")

    if unicode_chars:
        print(f"\nUnicode Characters ({len(unicode_chars)}):")
        for char in unicode_chars[:50]:  # Limit output
            print(f"  {repr(char)} (U+{ord(char):04X})")
        if len(unicode_chars) > 50:
            print(f"  ... and {len(unicode_chars) - 50} more")

    # Save full list to file
    output_file = TEMP_DIR / "base_characters.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for char in base_chars:
            f.write(f"{repr(char)}\t{char}\n")
    print(f"\n💾 Full list saved to: {output_file}")

    return base_chars


if __name__ == "__main__":
    base_chars = extract_base_characters()
