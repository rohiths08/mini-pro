#!/usr/bin/env python3
"""
Simple test script for flowchart generation
Run with: python test_flowchart.py
"""

import asyncio
import sys
sys.path.insert(0, './app')

from app.core.flowchart import generate_flowchart

async def test_flowchart():
    """Test flowchart generation with a simple function"""
    
    test_code = """
function sum(a, b) {
    return a + b;
}
"""
    
    print("Testing flowchart generation...")
    print("=" * 60)
    print("Input code:")
    print(test_code)
    print("=" * 60)
    
    result = await generate_flowchart(test_code, "javascript")
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
    else:
        print("\n✅ Generated Mermaid code:")
        print("-" * 60)
        print(result['mermaid'])
        print("-" * 60)
        
        # Validate it starts correctly
        mermaid = result['mermaid'].strip()
        if mermaid.startswith('flowchart') or mermaid.startswith('graph'):
            print("\n✅ Valid format: Starts with 'flowchart' or 'graph'")
        else:
            print(f"\n❌ Invalid format: Does not start correctly")
            print(f"First 100 chars: {mermaid[:100]}")

if __name__ == "__main__":
    asyncio.run(test_flowchart())
