import os
import tempfile
import subprocess
import pandas as pd
import textwrap
import json
import ast
import sys
import locale
from pathlib import Path
from radon.raw import analyze
from radon.complexity import cc_visit
from radon.metrics import mi_visit


def get_system_encoding():
    """Get the appropriate encoding for the current platform."""
    try:
        # Try to get system encoding
        encoding = locale.getpreferredencoding()
        if encoding.upper() != 'UTF-8':
            # Force UTF-8 for cross-platform compatibility
            return 'UTF-8'
        return encoding
    except:
        return 'UTF-8'


def safe_text_cleanup(text):
    """Safely clean text for cross-platform compatibility."""
    if text is None:
        return ""
    
    # Ensure we're working with a string
    text = str(text)
    
    # Replace problematic Unicode characters with ASCII equivalents
    unicode_replacements = {
        # Arrows and pointers
        '\u279e': '->',      # Heavy right-pointing angle bracket
        '\u2192': '->',      # Rightwards arrow
        '\u2190': '<-',      # Leftwards arrow
        '\u2191': '↑',       # Upwards arrow
        '\u2193': '↓',       # Downwards arrow
        '\u27f6': '=>',      # Long rightwards arrow
        
        # Dashes and hyphens
        '\u2013': '-',       # En dash
        '\u2014': '--',      # Em dash
        '\u2212': '-',       # Minus sign
        
        # Quotes
        '\u2018': "'",       # Left single quotation mark
        '\u2019': "'",       # Right single quotation mark
        '\u201c': '"',       # Left double quotation mark
        '\u201d': '"',       # Right double quotation mark
        '\u2032': "'",       # Prime
        '\u2033': '"',       # Double prime
        
        # Mathematical symbols
        '\u2260': '!=',      # Not equal to
        '\u2264': '<=',      # Less-than or equal to
        '\u2265': '>=',      # Greater-than or equal to
        '\u2217': '*',       # Asterisk operator
        '\u00f7': '/',       # Division sign
        
        # Other problematic characters
        '\u2026': '...',     # Horizontal ellipsis
        '\u00a0': ' ',       # Non-breaking space
        '\u200b': '',        # Zero-width space
    }
    
    cleaned = text
    for unicode_char, replacement in unicode_replacements.items():
        cleaned = cleaned.replace(unicode_char, replacement)
    
    return cleaned


def create_platform_temp_file(content, suffix=".py"):
    """Create a temporary file that works on all platforms."""
    encoding = get_system_encoding()
    
    try:
        # Clean content first
        cleaned_content = safe_text_cleanup(content)
        
        # Create temp file with platform-appropriate settings
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix=suffix,
            encoding=encoding,
            delete=False
        )
        temp_file.write(cleaned_content)
        temp_file.flush()
        temp_file.close()
        
        return temp_file.name
    except UnicodeEncodeError:
        # Fallback: use ASCII with replacement for really stubborn cases
        try:
            ascii_content = content.encode('ascii', 'replace').decode('ascii')
            temp_file = tempfile.NamedTemporaryFile(
                mode='w',
                suffix=suffix,
                encoding='ascii',
                delete=False
            )
            temp_file.write(ascii_content)
            temp_file.flush()
            temp_file.close()
            return temp_file.name
        except Exception as e:
            raise RuntimeError(f"Failed to create temp file: {e}")


def run_subprocess_platform(cmd, timeout=30):
    """Run subprocess with platform-independent settings."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding=get_system_encoding(),
            errors='replace'  # Replace encoding errors instead of crashing
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout running: {' '.join(cmd)}")
        return None
    except Exception as e:
        print(f"⚠️ Subprocess error: {e}")
        return None


def run_pylint(file_path):
    """Run pylint with platform-independent settings."""
    result = run_subprocess_platform([
        "pylint", 
        "--disable=all", 
        "--enable=E,F", 
        "--score=no", 
        file_path
    ])
    
    if result and result.returncode in [0, 1, 2, 4]:  # Pylint success/partial success codes
        error_count = result.stdout.count(": error")
        warning_count = result.stdout.count(": warning")
        return {"pylint_errors": error_count, "pylint_warnings": warning_count}
    
    return {"pylint_errors": None, "pylint_warnings": None}


def run_bandit(file_path):
    """Run Bandit with platform-independent settings."""
    result = run_subprocess_platform([
        "bandit", 
        "-q", 
        "-f", "json", 
        file_path
    ])
    
    if result and result.stdout.strip():
        try:
            report = json.loads(result.stdout)
            return len(report.get("results", []))
        except json.JSONDecodeError:
            return 0
    
    return 0


def calculate_cognitive_complexity_robust(code_str):
    """Robust cognitive complexity calculation."""
    try:
        score = 0
        lines = code_str.split('\n')
        nesting_level = 0
        
        for line in lines:
            stripped = safe_text_cleanup(line).strip()
            
            # Skip comments and empty lines
            if stripped.startswith('#') or not stripped:
                continue
                
            # Count control flow keywords
            control_keywords = ['if ', 'elif ', 'else:', 'for ', 'while ', 'except ', 'try:', 'with ']
            for keyword in control_keywords:
                if keyword in stripped:
                    score += 1 + nesting_level  # Nesting increases complexity
            
            # Track nesting level
            if stripped.endswith(':'):
                nesting_level += 1
            elif nesting_level > 0 and len(stripped) > 0 and len(stripped) - len(stripped.lstrip()) == 0:
                nesting_level = max(0, nesting_level - 1)
                
        return max(0, score)  # Ensure non-negative
    except Exception as e:
        print(f"⚠️ Cognitive complexity calculation error: {e}")
        return None


def safe_radon_analysis(code_str):
    """Safely run Radon analysis with comprehensive error handling."""
    try:
        # Clean the code first
        clean_code = safe_text_cleanup(code_str)
        
        # Parse to check syntax
        try:
            ast.parse(clean_code)
        except SyntaxError as e:
            print(f"⚠️ Syntax error in code: {e}")
            return None
        
        # Run Radon analysis
        raw_metrics = analyze(clean_code)
        cc_metrics = cc_visit(clean_code)
        mi_score = mi_visit(clean_code, multi=True)
        
        # Calculate average cyclomatic complexity
        if cc_metrics:
            total_complexity = sum(func.complexity for func in cc_metrics)
            avg_complexity = total_complexity / len(cc_metrics)
        else:
            avg_complexity = 0
        
        return {
            "loc": raw_metrics.loc,
            "lloc": raw_metrics.lloc, 
            "comments": raw_metrics.comments,
            "cyclomatic_complexity": avg_complexity,
            "maintainability_index": mi_score,
        }
        
    except Exception as e:
        print(f"⚠️ Radon analysis failed: {e}")
        return None


def analyze_single_problem(sample):
    """Analyze a single problem with full platform independence."""
    problem_id = sample["task_id"]
    prompt = sample.get("prompt", "")
    solution = sample.get("canonical_solution", "")
    
    # Initialize metrics with defaults
    metrics = {
        "problem_id": problem_id,
        "loc": None, "lloc": None, "comments": None,
        "cyclomatic_complexity": None, "maintainability_index": None,
        "cognitive_complexity": None, "pylint_errors": None,
        "pylint_warnings": None, "security_issues": None
    }
    
    # Skip if no solution
    if not solution or not solution.strip():
        print(f"⚠️ No solution for {problem_id}")
        return metrics
    
    temp_file_path = None
    
    try:
        # Reconstruct complete function
        complete_code = safe_text_cleanup(prompt) + "\n" + safe_text_cleanup(solution)
        
        # Create platform-independent temp file
        temp_file_path = create_platform_temp_file(complete_code)
        
        # Run analyses
        radon_results = safe_radon_analysis(complete_code)
        if radon_results:
            metrics.update(radon_results)
        
        # Run other analysis tools
        pylint_results = run_pylint(temp_file_path)
        metrics.update(pylint_results)
        
        metrics["security_issues"] = run_bandit(temp_file_path)
        metrics["cognitive_complexity"] = calculate_cognitive_complexity_robust(complete_code)
        
        # Determine success
        if metrics["loc"] is not None:
            print(f"✅ Analyzed {problem_id}")
        else:
            print(f"❌ Failed {problem_id}")
            
    except Exception as e:
        print(f"💥 Error analyzing {problem_id}: {e}")
        
    finally:
        # Cleanup temp file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                print(f"⚠️ Could not delete temp file {temp_file_path}: {e}")
    
    return metrics


def analyze_dataset(samples):
    """Analyze all samples with progress and error resilience."""
    results = []
    successful = 0
    total = len(samples)
    
    print(f"🔍 Starting analysis of {total} problems...")
    print(f"🌐 Platform: {sys.platform}")
    print(f"📝 Encoding: {get_system_encoding()}")
    
    for i, sample in enumerate(samples, 1):
        problem_id = sample["task_id"]
        print(f"[{i:3d}/{total}] Processing {problem_id}...")
        
        try:
            metrics = analyze_single_problem(sample)
            results.append(metrics)
            
            if metrics["loc"] is not None:
                successful += 1
                
        except Exception as e:
            print(f"💥 Critical error processing {problem_id}: {e}")
            # Add empty metrics to continue
            results.append({"problem_id": problem_id})
    
    success_rate = (successful / total) * 100
    print(f"\n📊 Analysis Complete:")
    print(f"   ✅ Successful: {successful}/{total} ({success_rate:.1f}%)")
    print(f"   ❌ Failed: {total - successful}/{total}")
    
    return pd.DataFrame(results)