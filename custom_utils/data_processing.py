from datasets import load_dataset, get_dataset_config_names, concatenate_datasets, Dataset
import pandas as pd
import os

class DataProcessing: 
    """A class to preprocess data"""
    
    @staticmethod
    def load_base_data_path(notebook_dir: str) -> str:
        """Path to data/"""
        return os.path.join(notebook_dir, "../data")
    
    @staticmethod
    def load_from_file(path: str, 
                       file_type: str = 'csv', 
                       sep: str = ",",
                       encoding: str = 'utf-8',
                       **kwargs):
        """Load data from directory
        
        Parameters
        ----------
        path : str
            Directory path where the file will be loaded from.
        file_type : str
            File types such as json, csv, parquet, xlsx, etc
        sep : str
            Delimiter for CSV files
        encoding : str
            File encoding
        **kwargs
            Additional keyword arguments passed to read functions
            (e.g., header=None, names=['col1', 'col2'], dtype=...)
        
        Returns
        -------
        pd.DataFrame or Dataset
            Loaded dataframe or dataset
        """
        
        if file_type == 'csv': 
            df = pd.read_csv(path, sep=sep, encoding=encoding, **kwargs)
            return df
        elif file_type == 'xlsx': 
            df = pd.read_excel(path, **kwargs)
            return df
        elif file_type == 'json':
            df = pd.read_json(path, **kwargs)
            return df
        elif file_type == 'parquet':
            df = pd.read_parquet(path, **kwargs)
            return df
        else:
            raise ValueError(f"Unsupported file_type: {file_type}")
    
    @staticmethod
    def load_pulselm_datasets(file_dir: str, dataset_names=None):
        """Load PulseLM dataset(s)
        
        Parameters
        ----------
        file_dir : str
            Directory containing the notebook
        dataset_names : str, list, or None
            - If str: load single dataset (e.g., 'wesad')
            - If list: load specific datasets (e.g., ['wesad', 'dalia'])
            - If None: load all datasets
            
        Returns
        -------
        pd.DataFrame or dict
            - If single dataset requested: returns DataFrame
            - If multiple datasets requested: returns dict with dataset names as keys
        """
        all_dataset_names = [
            'afppgecg', 'bcg', 'bidmc', 'dalia', 'earset', 'mimicperform',
            'ppgarrhythmia', 'ppgbp', 'sdb', 'sensors', 'uci', 'uqvitalsigns',
            'utsappg', 'vitaldb', 'wesad', 'wildppg'
        ]
        
        base_data_path = DataProcessing.load_base_data_path(file_dir)
        
        # Handle single dataset (string input)
        if isinstance(dataset_names, str):
            dataset_path = os.path.join(base_data_path, "pulselm", f"{dataset_names}.parquet")
            return DataProcessing.load_from_file(dataset_path, file_type='parquet')
        
        # Handle multiple datasets (list or None)
        if dataset_names is None:
            dataset_names = all_dataset_names
        
        datasets = {}
        for name in dataset_names:
            try:
                dataset_path = os.path.join(base_data_path, "pulselm", f"{name}.parquet")
                datasets[name] = DataProcessing.load_from_file(dataset_path, file_type='parquet')
                print(f"Loaded {name}: {len(datasets[name])} samples")
            except Exception as e:
                print(f"Error loading {name}: {e}")
        
        return datasets
    
    @staticmethod
    def load_afppgecg(file_dir: str, filename: str = "pulselm_combined.parquet"):
        """Load the AF-PPG-ECG dataset from parquet file (legacy method)
        
        Parameters
        ----------
        file_dir : str
            Directory containing the notebook
        filename : str
            Name of the parquet file
            
        Returns
        -------
        pd.DataFrame
            Loaded dataframe
        """
        base_data_path = DataProcessing.load_base_data_path(file_dir)
        dataset_path = os.path.join(base_data_path, filename)
        return DataProcessing.load_from_file(dataset_path, file_type='parquet')