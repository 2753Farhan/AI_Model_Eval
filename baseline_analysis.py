import os
import pandas as pd
import sys
import locale
from src.data_layer.config_manager import ConfigManager
from src.data_layer.dataset_loader import HumanEvalLoader
from src.analysis_layer.static_analysis import analyze_dataset


def setup_cross_platform_environment():
    """Set up environment for cross-platform compatibility."""
    print("🌐 Setting up cross-platform environment...")
    
    # Force UTF-8 encoding globally
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf-8')
    
    # Set environment variables for UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    try:
        # Set locale to UTF-8 if available
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except locale.Error:
            print("⚠️ Could not set UTF-8 locale, using system default")
    
    print(f"📝 Python version: {sys.version}")
    print(f"🔧 Platform: {sys.platform}")
    print(f"💾 Encoding: {sys.getdefaultencoding()}")


def main():
    print("🚀 Starting Milestone 1: Human Baseline Establishment")
    
    # Set up cross-platform environment
    setup_cross_platform_environment()
    
    try:
        # Load config
        config = ConfigManager("config/settings.yaml")
        config.ensure_dirs()

        repo_url = config.get("paths.repo_url")
        data_dir = config.get("paths.data_dir")
        results_dir = config.get("paths.results_dir")

        # Fetch dataset
        print("📥 Setting up dataset...")
        loader = HumanEvalLoader(repo_url, data_dir)
        loader.fetch_repo()
        samples = loader.load_dataset()

        # Perform static analysis
        print("🔧 Running static analysis tools...")
        df = analyze_dataset(samples)

        # Save results with platform-independent settings
        os.makedirs(results_dir, exist_ok=True)
        output_path = os.path.join(results_dir, "human_baseline_metrics.csv")
        
        # Save with UTF-8 encoding for cross-platform compatibility
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        # Generate summary
        successful = len(df[df['loc'].notna()])
        total = len(df)
        
        summary_path = os.path.join(results_dir, "baseline_summary.txt")
        with open(summary_path, "w", encoding='utf-8') as f:
            f.write("Human Baseline Metrics Summary\n")
            f.write("=" * 40 + "\n")
            f.write(f"Platform: {sys.platform}\n")
            f.write(f"Total problems: {total}\n")
            f.write(f"Successful analyses: {successful}\n")
            f.write(f"Failed analyses: {total - successful}\n")
            f.write(f"Success rate: {(successful/total)*100:.1f}%\n\n")
            
            if successful > 0:
                numeric_cols = df.select_dtypes(include=['number']).columns
                for col in numeric_cols:
                    if df[col].notna().any():
                        valid_data = df[col].dropna()
                        f.write(f"{col}:\n")
                        f.write(f"  Mean: {valid_data.mean():.2f}\n")
                        f.write(f"  Std:  {valid_data.std():.2f}\n")
                        f.write(f"  Min:  {valid_data.min():.2f}\n")
                        f.write(f"  Max:  {valid_data.max():.2f}\n\n")

        print(f"✅ Baseline metrics saved to: {output_path}")
        print(f"✅ Summary statistics saved to: {summary_path}")
        
        # Final report
        print(f"\n🎉 MILESTONE 1 COMPLETE!")
        print(f"📊 Successfully analyzed {successful}/{total} problems")
        if successful > 0:
            print(f"📍 Average LOC: {df['loc'].mean():.1f}")
            print(f"📍 Average Complexity: {df['cyclomatic_complexity'].mean():.1f}")
            print(f"📍 Average Maintainability: {df['maintainability_index'].mean():.1f}")
        
    except Exception as e:
        print(f"💥 Critical error in baseline analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()