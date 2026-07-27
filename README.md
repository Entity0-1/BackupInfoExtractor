# BackupInfoExtractor
Small program to extract voice memos and notes from an IPhone backup folder after backing up your IPhone to a pc/mac

At line 8 change the path to your IPhone backup folder path on your pc/mac

If you never connected your voice memos to ICloud then you may need to change line 34-39 to the following:

query = """
    SELECT fileID, domain, relativePath 
    FROM Files 
    WHERE relativePath LIKE '%NoteStore.sqlite%' 
       OR relativePath LIKE 'Media/Recordings/%.m4a'
    """
