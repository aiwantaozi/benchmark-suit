#!/usr/bin/env python3
"""
Automated Inference Engine Performance Testing Framework
Supports performance comparison of vLLM, SGLang, TRT-LLM and other engines
"""

import os
import sys
import yaml
import time
import json
import signal
import logging
import subprocess
import threading
import copy
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("llm_benchmark")

class EngineType(Enum):
    """Supported inference engine types"""
    VLLM = "vllm"
    SGLANG = "sglang"
    TRTLLM = "trtllm"

class TestCaseType(Enum):
    """Types of benchmark test cases"""
    SHAREGPT = "sharegpt"
    RANDOM = "random"

@dataclass
class TestCase:
    """Configuration for a single test case"""
    name: str
    type: TestCaseType
    dataset_path: Optional[str] = None
    random_input_len: Optional[int] = None
    random_output_len: Optional[int] = None
    num_prompts: int = 100
    seed: int = 42
    result_filename: Optional[str] = None

def get_default_test_case_templates() -> Dict[str, Dict]:
    return {
        "sharegpt": {
            "type": "sharegpt",
            "num_prompts": 1000,
            "dataset_path": "ShareGPT_V3_unfiltered_cleaned_split.json"
        },
        "random_32k": {
            "type": "random",
            "input_len": 32000,
            "output_len": 100,
            "num_prompts": 100,
            "seed": 42
        },
        "random_4k": {
            "type": "random",
            "input_len": 4000,
            "output_len": 200,
            "num_prompts": 500,
            "seed": 42
        },
        "random_2k": {
            "type": "random",
            "input_len": 2000,
            "output_len": 100,
            "num_prompts": 500,
            "seed": 42
        },
        "random_128": {
            "type": "random",
            "input_len": 128,
            "output_len": 4,
            "num_prompts": 1000,
            "seed": 42
        },
        "random_2k_output": {
            "type": "random",
            "input_len": 1000,
            "output_len": 2000,
            "num_prompts": 100,
            "seed": 42
        }
    }

@dataclass
class EngineConfig:
    """Configuration for an engine test run"""
    name: str
    engine: EngineType
    test_cases: List[TestCase]
    envs: Dict[str, str] = None
    args: str = ""
    port: int = 8000
    conda_env: Optional[str] = None

@dataclass
class BenchmarkResult:
    """Results from a single benchmark run"""
    config_name: str
    engine: str
    test_case: str
    result_file: str
    timestamp: str
    metrics: Dict[str, Any] = None

class EngineManager:
    """Manages startup and shutdown of different inference engines"""
    
    def __init__(self, model_path: str, output_dir: str = "benchmark_results"):
        self.model_path = model_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.current_process = None
        self.results: List[BenchmarkResult] = []
        
    def setup_environment(self, envs: Dict[str, str]):
        """Set environment variables for the engine"""
        if envs:
            for key, value in envs.items():
                os.environ[key] = value
                logger.info(f"Set env {key}={value}")
    
    def run_command(self, command: str, conda_env: Optional[str] = None, wait: bool = True):
        """Execute shell command with optional conda environment"""
        if conda_env:
            command = f"conda run -n {conda_env} {command}"
        
        logger.info(f"Running command: {command}")
        
        if wait:
            # For blocking commands that should complete before continuing
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Command failed: {result.stderr}")
                raise RuntimeError(f"Command failed with return code {result.returncode}")
            return result
        else:
            # For non-blocking server startup commands
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.current_process = process
            
            # Start monitoring thread to check service readiness
            monitor_thread = threading.Thread(target=self._monitor_service_startup, args=(process,))
            monitor_thread.daemon = True
            monitor_thread.start()
            
            return process
    
    def _monitor_service_startup(self, process, max_wait=60):
        """Monitor service startup process and check when it's ready"""
        start_time = time.time()
        while time.time() - start_time < max_wait:
            if process.poll() is not None:
                # Process has terminated
                stdout, stderr = process.communicate()
                logger.error(f"Service failed to start: {stderr}")
                return
            
            # Check if port is ready (simple implementation)
            try:
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex(('localhost', 8000))
                s.close()
                if result == 0:
                    logger.info("Service is ready on port 8000")
                    return
            except:
                pass
            
            time.sleep(2)
        
        logger.warning("Service startup monitoring timeout")
    
    def start_vllm(self, config: EngineConfig):
        """Start vLLM inference server"""
        cmd = f"vllm serve {self.model_path} {config.args} --port {config.port}"
        self.run_command(cmd, config.conda_env, wait=False)
        time.sleep(10)  # Wait for service to initialize
    
    def start_sglang(self, config: EngineConfig):
        """Start SGLang inference server"""
        cmd = f"python -m sglang.launch_server --model-path {self.model_path} --host 0.0.0.0 --port {config.port} {config.args}"
        self.run_command(cmd, config.conda_env, wait=False)
        time.sleep(15)  # SGLang may need longer startup time
    
    def start_trtllm(self, config: EngineConfig):
        """Start TRT-LLM inference server"""
        cmd = f"trtllm-serve {self.model_path} {config.args}"
        self.run_command(cmd, config.conda_env, wait=False)
        time.sleep(20)  # TRT-LLM typically needs longer startup time
    
    def stop_current_service(self):
        """Stop currently running inference service"""
        if self.current_process:
            try:
                # Send SIGTERM signal
                self.current_process.terminate()
                try:
                    # Wait for process to terminate
                    self.current_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    # Force kill if timeout
                    self.current_process.kill()
                    self.current_process.wait()
                
                logger.info("Successfully stopped current service")
            except Exception as e:
                logger.error(f"Error stopping service: {e}")
            finally:
                self.current_process = None
    
    def run_benchmark(self, test_case: TestCase, result_filename: str):
        """Execute performance benchmark for given test case"""
        base_cmd = f"vllm bench serve --model {self.model_path} --endpoint-type openai-chat --endpoint http://localhost:8000/v1/chat/completions"
        
        if test_case.type == TestCaseType.SHAREGPT:
            if not test_case.dataset_path:
                # Automatically download dataset if not present
                dataset_path = self.download_sharegpt_dataset()
                test_case.dataset_path = dataset_path
            
            cmd = f"{base_cmd} --dataset-name sharegpt --dataset-path {test_case.dataset_path} --num-prompts {test_case.num_prompts}"
        
        elif test_case.type == TestCaseType.RANDOM:
            cmd = f"{base_cmd} --dataset-name random --random-input-len {test_case.random_input_len} --random-output-len {test_case.random_output_len} --num-prompts {test_case.num_prompts} --seed {test_case.seed}"
        
        cmd += f" --result-filename {result_filename}"
        
        logger.info(f"Running benchmark: {test_case.name}")
        result = self.run_command(cmd, "vllm")
        
        return result
    
    def download_sharegpt_dataset(self):
        """Download ShareGPT dataset if not already present"""
        dataset_path = Path("ShareGPT_V3_unfiltered_cleaned_split.json")
        if not dataset_path.exists():
            logger.info("Downloading ShareGPT dataset...")
            cmd = "wget https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json"
            self.run_command(cmd)
        return str(dataset_path)
    
    def parse_results(self, result_file: str) -> Dict[str, Any]:
        """Parse and extract metrics from benchmark result file"""
        result_path = Path(result_file)
        if result_path.exists():
            with open(result_path, 'r') as f:
                data = json.load(f)
            return data
        return {}
    
    def run_engine_test(self, config: EngineConfig):
        """Execute complete test suite for specified engine configuration"""
        logger.info(f"Starting test for {config.name}")
        
        try:
            # Set environment variables
            if config.envs:
                self.setup_environment(config.envs)
            
            # Start inference server based on engine type
            if config.engine == EngineType.VLLM:
                self.start_vllm(config)
            elif config.engine == EngineType.SGLANG:
                self.start_sglang(config)
            elif config.engine == EngineType.TRTLLM:
                self.start_trtllm(config)
            
            # Execute all test cases for this engine
            for test_case in config.test_cases:
                # Generate result filename if not provided
                if test_case.result_filename:
                    result_filename = test_case.result_filename
                else:
                    result_filename = f"{config.name.replace('-', '_')}_{test_case.name}.json"
                
                result_path = self.output_dir / result_filename
                
                self.run_benchmark(test_case, str(result_path))
                
                # Record results
                result = BenchmarkResult(
                    config_name=config.name,
                    engine=config.engine.value,
                    test_case=test_case.name,
                    result_file=str(result_path),
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                    metrics=self.parse_results(result_path)
                )
                self.results.append(result)
                
                logger.info(f"Completed test case: {test_case.name}")
        
        except Exception as e:
            logger.error(f"Error running test {config.name}: {e}")
            raise
        finally:
            # Ensure service is stopped even if test fails
            self.stop_current_service()
            time.sleep(5)  # Wait for resource cleanup
    
    def generate_report(self):
        """Generate comprehensive test report with all results"""
        report_file = self.output_dir / f"benchmark_report_{int(time.time())}.json"
        
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model": self.model_path,
            "results": [asdict(result) for result in self.results]
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Report generated: {report_file}")
        return report_file

def load_config(config_file: str) -> Dict[str, Any]:
    """Load YAML configuration file"""
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

def create_test_case_from_dict(name: str, tc_config: Dict) -> TestCase:
    """Create a TestCase object from configuration dictionary"""
    if tc_config['type'] == 'sharegpt':
        test_case = TestCase(
            name=name,
            type=TestCaseType.SHAREGPT,
            dataset_path=tc_config.get('dataset_path'),
            num_prompts=tc_config.get('num_prompts', 1000),
            result_filename=tc_config.get('result_filename')
        )
    elif tc_config['type'] == 'random':
        test_case = TestCase(
            name=name,
            type=TestCaseType.RANDOM,
            random_input_len=tc_config['input_len'],
            random_output_len=tc_config['output_len'],
            num_prompts=tc_config.get('num_prompts', 100),
            seed=tc_config.get('seed', 42),
            result_filename=tc_config.get('result_filename')
        )
    else:
        raise ValueError(f"Unknown test case type: {tc_config['type']}")
    
    return test_case

def create_engine_configs_from_config(config: Dict) -> List[EngineConfig]:
    """Create EngineConfig objects from configuration data"""
    engine_configs = []
    
    # Create test case templates dictionary
    test_case_templates = get_default_test_cases()
    
    if 'test_cases' in config:
        test_case_templates = {}
        for name, tc_config in config['test_cases'].items():
            test_case_templates[name] = create_test_case_from_dict(name, tc_config)
    
    # Create baseline vLLM configuration if enabled
    if config.get('run_baseline', True):
        baseline_test_cases = []
        
        # Use all test cases for baseline
        for name, test_case in test_case_templates.items():
            # Create a copy to avoid modifying the template
            baseline_test_case = copy.deepcopy(test_case)
            baseline_test_cases.append(baseline_test_case)
        
        baseline_config = EngineConfig(
            name="vllm-baseline",
            engine=EngineType.VLLM,
            test_cases=baseline_test_cases,
            args=config.get('baseline_args', ''),
            conda_env="vllm"
        )
        engine_configs.append(baseline_config)
    
    # Process custom run configurations
    for run_config in config.get('runs', []):
        test_cases = []
        
        # Get test cases by name from templates
        for test_case_name in run_config.get('test_cases', []):
            if test_case_name in test_case_templates:
                # Create a copy of the template test case
                test_case = copy.deepcopy(test_case_templates[test_case_name])
                test_cases.append(test_case)
            else:
                logger.warning(f"Test case '{test_case_name}' not found in templates, skipping")
        
        engine_config = EngineConfig(
            name=run_config['name'],
            engine=EngineType(run_config['engine']),
            test_cases=test_cases,
            envs=run_config.get('envs', {}),
            args=run_config.get('args', ''),
            port=run_config.get('port', 8000),
            conda_env=run_config.get('conda_env')
        )
        engine_configs.append(engine_config)
    
    return engine_configs

def main():
    """Main entry point for the benchmark tool"""
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM Inference Engine Automated Performance Testing")
    parser.add_argument("--config", "-c", default="config.yaml", help="Path to configuration YAML file")
    parser.add_argument("--model", "-m", help="Model path (overrides config model)")
    parser.add_argument("--output-dir", "-o", default="benchmark_results", help="Output directory for results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load configuration
    config = load_config(args.config)
    model_path = args.model or config['model']
    
    # Create engine manager
    manager = EngineManager(model_path, args.output_dir)
    
    # Create engine configurations from YAML
    engine_configs = create_engine_configs_from_config(config)
    
    # Execute all benchmark tests
    for engine_config in engine_configs:
        try:
            manager.run_engine_test(engine_config)
            logger.info(f"Successfully completed test: {engine_config.name}")
        except Exception as e:
            logger.error(f"Failed to run test {engine_config.name}: {e}")
            # Continue with other tests even if one fails
    
    # Generate final report
    report_file = manager.generate_report()
    logger.info(f"All tests completed. Report: {report_file}")

if __name__ == "__main__":
    main()
