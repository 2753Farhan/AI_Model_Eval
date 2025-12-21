import pandas as pd
from typing import List, Dict
import logging
from tqdm import tqdm
import time

logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self, model_manager, prompt_engine):
        self.model_manager = model_manager
        self.prompt_engine = prompt_engine
    
    def generate_solutions(self, problems: List[Dict], models: List[str], 
                         num_samples: int = 5, strategies: List[str] = None) -> pd.DataFrame:
        """Generate solutions for all problems with different models and strategies"""
        if strategies is None:
            strategies = ["zero_shot"]
        
        all_solutions = []
        
        for problem in tqdm(problems, desc="🔄 Processing problems"):
            for model in models:
                for strategy in strategies:
                    for sample_idx in range(num_samples):
                        try:
                            # Format prompt
                            prompt = self.prompt_engine.format_prompt(problem, strategy)
                            
                            # Generate code
                            generated_code = self.model_manager.generate_code(prompt, model)
                            
                            # Store solution
                            solution = {
                                'task_id': problem['task_id'],
                                'problem_id': problem['task_id'].split('/')[-1],
                                'model': model,
                                'strategy': strategy,
                                'sample_id': sample_idx,
                                'prompt': prompt,
                                'generated_code': generated_code,
                                'original_solution': problem.get('canonical_solution', ''),
                                'tests': problem.get('test', '')
                            }
                            all_solutions.append(solution)
                            
                            # Small delay to avoid rate limits
                            time.sleep(0.5)
                            
                        except Exception as e:
                            logger.error(f"❌ Generation failed for {problem['task_id']}: {e}")
                            # Add error entry
                            all_solutions.append({
                                'task_id': problem['task_id'],
                                'problem_id': problem['task_id'].split('/')[-1],
                                'model': model,
                                'strategy': strategy,
                                'sample_id': sample_idx,
                                'prompt': '',
                                'generated_code': f'# Generation error: {str(e)}',
                                'original_solution': '',
                                'tests': '',
                                'error': str(e)
                            })
        
        return pd.DataFrame(all_solutions)