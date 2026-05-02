import os
import sys
import json
import time
from typing import List, Dict
from analyzer.slop_engine import SlopEngine

def run_batch(directory: str, engine: SlopEngine) -> List[Dict]:
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.c', '.cpp', '.h', '.hpp')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    start_time = time.time()
                    analysis = engine.analyze(content, "auto", file_path)
                    duration = time.time() - start_time
                    
                    results.append({
                        "file": os.path.relpath(file_path, directory),
                        "score": round(analysis.final_score, 2),
                        "findings": len([f for p in analysis.pillars for f in p.findings]),
                        "duration": round(duration, 3),
                        "status": "SLOP" if analysis.final_score > 50 else "CLEAN"
                    })
                except Exception as e:
                    results.append({
                        "file": os.path.relpath(file_path, directory),
                        "error": str(e)
                    })
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No directory specified"}))
        sys.exit(1)
        
    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(json.dumps({"error": f"Not a directory: {target_dir}"}))
        sys.exit(1)
        
    engine = SlopEngine()
    results = run_batch(target_dir, engine)
    print(json.dumps(results, indent=2))
