try:
    from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
    from langchain_community.document_loaders import DirectoryLoader
    print("Imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Other error: {e}")