import re


def fix_text_spacing(text: str) -> str:
    """
    Fix improper spacing in text that may come from PDF extraction or API responses.
    
    Handles cases like:
    - "connect i on" -> "connection"
    - "be tween" -> "between"
    - "T h is" -> "This"
    - "a nd" -> "and"
    """
    if not text or not isinstance(text, str):
        return text
    
    # Step 1: Fix single character words that are likely part of a larger word
    # Pattern: word boundary + single letter + space + single letter (repeated)
    # This handles cases like "c o n n e c t i o n" -> "connection"
    text = re.sub(r'\b([a-zA-Z])\s+(?=[a-zA-Z]\s)', r'\1', text)
    
    # Step 2: Fix remaining single letter + space + letters pattern
    # This handles "i on" -> "ion", "a nd" -> "and", etc.
    text = re.sub(r'\b([a-zA-Z])\s+([a-zA-Z]{1,2})\b', r'\1\2', text)
    
    # Step 3: Fix split words where there's a space in the middle
    # Pattern: lowercase letter + space + lowercase letter(s) at word boundaries
    # This catches "connect ion" -> "connection"
    text = re.sub(r'([a-z]{2,})\s+([a-z]{1,3})(?=\s|[.,;:!?]|$)', r'\1\2', text)
    
    # Step 4: Fix capital letter followed by space and lowercase letters
    # "T his" -> "This", "I n" -> "In"
    text = re.sub(r'\b([A-Z])\s+([a-z]+)\b', r'\1\2', text)
    
    # Step 5: Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Step 6: Fix spacing around punctuation
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    text = re.sub(r'([.,;:!?])(?=[A-Za-z])', r'\1 ', text)
    
    # Step 7: Fix common word fragments
    common_fixes = {
        r'\bw he re\b': 'where',
        r'\bw he n\b': 'when',
        r'\bw h at\b': 'what',
        r'\bw h ich\b': 'which',
        r'\bt he\b': 'the',
        r'\bt h is\b': 'this',
        r'\bt h at\b': 'that',
        r'\bt he se\b': 'these',
        r'\bt he re\b': 'there',
        r'\bt he ir\b': 'their',
        r'\bt he y\b': 'they',
        r'\ba nd\b': 'and',
        r'\bf or\b': 'for',
        r'\bf rom\b': 'from',
        r'\bw ith\b': 'with',
        r'\bw ithout\b': 'without',
        r'\bb e\b': 'be',
        r'\bb een\b': 'been',
        r'\bb eing\b': 'being',
        r'\bh ave\b': 'have',
        r'\bh as\b': 'has',
        r'\bh ad\b': 'had',
        r'\bd o\b': 'do',
        r'\bd oes\b': 'does',
        r'\bd id\b': 'did',
        r'\bc an\b': 'can',
        r'\bc ould\b': 'could',
        r'\bw ould\b': 'would',
        r'\bs hould\b': 'should',
        r'\bm ay\b': 'may',
        r'\bm ight\b': 'might',
        r'\bm ust\b': 'must',
        r'\bs hall\b': 'shall',
        r'\bw ill\b': 'will',
        r'\ba re\b': 'are',
        r'\bi s\b': 'is',
        r'\bw as\b': 'was',
        r'\bw ere\b': 'were',
        r'\bi n\b': 'in',
        r'\bo n\b': 'on',
        r'\ba t\b': 'at',
        r'\bb y\b': 'by',
        r'\bt o\b': 'to',
        r'\bo f\b': 'of',
        r'\ba s\b': 'as',
        r'\bi t\b': 'it',
        r'\bi f\b': 'if',
        r'\bo r\b': 'or',
        r'\bn o\b': 'no',
        r'\bn ot\b': 'not',
        r'\bs o\b': 'so',
        r'\bu p\b': 'up',
        r'\bo ut\b': 'out',
        r'\ba ll\b': 'all',
        r'\ba ny\b': 'any',
        r'\bb ut\b': 'but',
        r'\bg et\b': 'get',
        r'\bg ot\b': 'got',
        r'\bp ut\b': 'put',
        r'\bs et\b': 'set',
        r'\bu se\b': 'use',
        r'\bu sed\b': 'used',
        r'\bh ow\b': 'how',
        r'\bn ow\b': 'now',
        r'\bn ew\b': 'new',
        r'\bo ld\b': 'old',
        r'\bo ne\b': 'one',
        r'\bt wo\b': 'two',
        r'\bs ee\b': 'see',
        r'\bs een\b': 'seen',
        r'\bm ake\b': 'make',
        r'\bm ade\b': 'made',
        r'\bg o\b': 'go',
        r'\bg one\b': 'gone',
        r'\bc ome\b': 'come',
        r'\bt ake\b': 'take',
        r'\bt ook\b': 'took',
        r'\bt aken\b': 'taken',
    }
    
    for pattern, replacement in common_fixes.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Step 8: Final cleanup - remove any remaining multiple spaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def format_response_text(text: str) -> str:
    """
    Main function to format API response text.
    Applies all necessary text corrections.
    """
    return fix_text_spacing(text)
