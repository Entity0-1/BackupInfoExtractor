# BackupInfoExtractor
A simple program to extract Voice Memos and Notes from your local iPhone backup folder.

I built this to bypass Apple's restrictive file mapping. Instead of saving your backup in standard folders, iOS scrambles the filenames and relies on an internal database to map them. This script reads that map, finds your files, and exports them so you **actually** have access to your own data.

At line 8 change the path to your IPhone backup folder path on your pc/mac

If you never connected your voice memos to ICloud then you may need to change line 34-39 to the following:

query = """
    SELECT fileID, domain, relativePath 
    FROM Files 
    WHERE relativePath LIKE '%NoteStore.sqlite%' 
       OR relativePath LIKE 'Media/Recordings/%.m4a'
    """

Apple automatically turns on ICloud sharing for all your apps and the second it does it changes the file mapping for voice memos which is why that might be necessary. 
Possible plans in the future to make that moot. 
