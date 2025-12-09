# %%
# Imports
from typing import List

# %%
# Chunker
def chunk_text(
        text: str,
        chunk_size: int=500,
        overlap: int=50
)-> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: The text to chunk
        chunk_size: Target size of each chunk (in characters)
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if len(text)<=chunk_size:
        return [text]
    else:
        chunked=[]
        while len(text)>chunk_size:
            chunked.append(text[:chunk_size])
            text=text[(chunk_size-overlap):]
        if len(text)>0:
            chunked.append(text)
    return chunked
