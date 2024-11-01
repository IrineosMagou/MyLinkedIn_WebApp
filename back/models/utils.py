import importlib

# List of module names to import from
module_names = [
    'models.AdminModels',
    'models.AdsModels',
    'models.ArticleModels',
    'models.models_user',
]

# Initialize an empty __all__ list
__all__ = []

# Loop over each module name and dynamically import the module
for module_name in module_names:
    module = importlib.import_module(module_name)  # Dynamically import the module
    
    # Get the current module's public attributes and append to __all__
    public_names = [name for name in dir(module) if not name.startswith('_')]
    __all__.extend(public_names)

    # Add the module's symbols to the current namespace (optional)
    globals().update({name: getattr(module, name) for name in public_names})

# Now __all__ contains all the public symbols from all modules.
